"""Session revert for undoing changes."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from ..backends.snapshot import SnapshotBackend, Patch
from ..backends.state import StateBackend


@dataclass
class RevertState:
    """State of a revert operation."""
    block_id: str
    snapshot_id: str
    diff: str = ""
    reverted_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "block_id": self.block_id,
            "snapshot_id": self.snapshot_id,
            "diff": self.diff,
            "reverted_at": self.reverted_at.isoformat(),
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> RevertState:
        return cls(
            block_id=data["block_id"],
            snapshot_id=data["snapshot_id"],
            diff=data.get("diff", ""),
            reverted_at=datetime.fromisoformat(data["reverted_at"])
            if "reverted_at" in data else datetime.now(),
        )


class SessionRevert:
    """Manage session reverts.
    
    Handles reverting to previous states, including:
    - File system changes (via snapshot)
    - Session blocks
    - Memory entries (if integrated)
    """
    
    def __init__(
        self,
        storage: StateBackend,
        snapshot: SnapshotBackend | None = None,
    ):
        self.storage = storage
        self.snapshot = snapshot
        self._revert_states: dict[str, RevertState] = {}  # session_id -> RevertState
    
    async def revert(
        self,
        session_id: str,
        block_id: str,
        branch: str | None = None,
    ) -> RevertState:
        """Revert session to state before specified block.
        
        Args:
            session_id: Session to revert
            block_id: Revert to state before this block
            branch: Optional branch filter (None = all branches)
            
        Returns:
            RevertState with revert info
        """
        # 1. Record current state for unrevert
        current_snapshot = None
        if self.snapshot:
            current_snapshot = await self.snapshot.track()
        
        # 2. Get block info
        block_data = await self.storage.read(["sessions", session_id, "blocks", block_id])
        if not block_data:
            raise ValueError(f"Block not found: {block_id}")
        
        target_snapshot = block_data.get("snapshot_id")
        
        # 3. Collect patches to revert
        blocks_after = await self._get_blocks_after(session_id, block_id, branch)
        
        if self.snapshot and blocks_after:
            patches = []
            for block in blocks_after:
                if "patch" in block.get("data", {}):
                    patches.append(Patch.from_dict(block["data"]["patch"]))
            
            if patches:
                await self.snapshot.revert(patches)
        
        # 4. Get diff
        diff = ""
        if self.snapshot and target_snapshot:
            diff = await self.snapshot.diff(target_snapshot)
        
        # 5. Create revert state
        revert_state = RevertState(
            block_id=block_id,
            snapshot_id=current_snapshot or "",
            diff=diff,
        )
        
        # 6. Store revert state
        self._revert_states[session_id] = revert_state
        await self.storage.write(
            ["sessions", session_id, "revert"],
            revert_state.to_dict(),
        )
        
        return revert_state
    
    async def unrevert(self, session_id: str) -> bool:
        """Undo a revert operation.
        
        Args:
            session_id: Session to unrevert
            
        Returns:
            True if unrevert was performed
        """
        revert_state = self._revert_states.get(session_id)
        
        if not revert_state:
            # Try loading from storage
            stored = await self.storage.read(["sessions", session_id, "revert"])
            if stored:
                revert_state = RevertState.from_dict(stored)
        
        if not revert_state:
            return False
        
        # Restore to snapshot before revert
        if self.snapshot and revert_state.snapshot_id:
            await self.snapshot.restore(revert_state.snapshot_id)
        
        # Clear revert state
        self._revert_states.pop(session_id, None)
        await self.storage.remove(["sessions", session_id, "revert"])
        
        return True
    
    async def cleanup(self, session_id: str) -> int:
        """Clean up revert state after new prompt.
        
        Deletes blocks after the revert point.
        
        Args:
            session_id: Session to cleanup
            
        Returns:
            Number of blocks deleted
        """
        revert_state = self._revert_states.get(session_id)
        
        if not revert_state:
            stored = await self.storage.read(["sessions", session_id, "revert"])
            if stored:
                revert_state = RevertState.from_dict(stored)
        
        if not revert_state:
            return 0
        
        # Get blocks to delete
        blocks_to_delete = await self._get_blocks_after(
            session_id,
            revert_state.block_id,
        )
        
        # Delete blocks
        deleted = 0
        for block in blocks_to_delete:
            await self.storage.remove(
                ["sessions", session_id, "blocks", block["id"]]
            )
            deleted += 1
        
        # Clear revert state
        self._revert_states.pop(session_id, None)
        await self.storage.remove(["sessions", session_id, "revert"])
        
        return deleted
    
    async def _get_blocks_after(
        self,
        session_id: str,
        block_id: str,
        branch: str | None = None,
    ) -> list[dict[str, Any]]:
        """Get all blocks after specified block."""
        # Get target block timestamp
        target = await self.storage.read(
            ["sessions", session_id, "blocks", block_id]
        )
        if not target:
            return []
        
        target_time = target.get("created_at", "")
        
        # Find all blocks after
        all_blocks = await self.storage.find(
            ["sessions", session_id, "blocks"],
            filter={},
            sort=[("created_at", 1)],
        )
        
        blocks_after = []
        found_target = False
        
        for block in all_blocks:
            if block.get("id") == block_id:
                found_target = True
                continue
            
            if found_target:
                # Apply branch filter
                if branch is None or block.get("branch") == branch:
                    blocks_after.append(block)
        
        return blocks_after
    
    def get_revert_state(self, session_id: str) -> RevertState | None:
        """Get current revert state for session."""
        return self._revert_states.get(session_id)
    
    def is_reverted(self, session_id: str) -> bool:
        """Check if session is in reverted state."""
        return session_id in self._revert_states
