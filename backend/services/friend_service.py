"""
Friend service for friendship management

Built by: Max Quirk and Jamie Morrone
"""

from models.friend import Friend

class FriendService:
    """Handles friendship logic"""

    def __init__(self, friend_repo, user_repo):
        self.friend_repo = friend_repo
        self.user_repo = user_repo

    def remove_friend(self, user_id, friend_id):
        """
        Remove a friend relationship.
        Works regardless of who initiated the friendship.
        """
        # Find the friendship
        friendship = self.friend_repo.find_friendship(user_id, friend_id)
        if not friendship:
            raise ValueError("Friendship not found")

        # Remove the friendship
        self.friend_repo.remove(friendship.id)
        return True

    def send_friend_request(self, user_id, friend_email):
        """
        Send a friend request to another user by email.
        Returns (success: bool, message: str, friend_id: str or None)
        """
        # Check if current user exists
        user = self.user_repo.find_by_id(user_id)
        if user is None:
            return False, "User not found", None

        # Find friend by email
        friend_user = self.user_repo.find_by_email(friend_email)
        if friend_user is None:
            return False, "No user found with that email address", None

        # Check if trying to add self as friend
        if user_id == friend_user.id:
            return False, "Cannot send a friend request to yourself", None

        # Check if friendship already exists
        existing = self.friend_repo.find_friendship(user_id, friend_user.id)
        if existing:
            if existing.status == 'pending':
                return False, "Friend request already sent or received", None
            elif existing.status == 'accepted':
                return False, "Already friends with this user", None

        # Send the friend request
        self.friend_repo.send_friend_request(user_id, friend_user.id)
        return True, "Friend request sent successfully", friend_user.id

    def accept_friend_request(self, user_id, request_id):
        """
        Accept a friend request.
        Returns (success: bool, message: str)
        """
        # Get the friend request
        friendship = self.friend_repo.find_by_id(request_id)
        if not friendship:
            return False, "Friend request not found"

        # Verify that the current user is the recipient
        if friendship.friend_id != user_id:
            return False, "You cannot accept this friend request"

        # Verify it's pending
        if friendship.status != 'pending':
            return False, "This friend request is not pending"

        # Accept the request
        self.friend_repo.accept_friend_request(request_id)
        return True, "Friend request accepted"

    def reject_friend_request(self, user_id, request_id):
        """
        Reject a friend request.
        Returns (success: bool, message: str)
        """
        # Get the friend request
        friendship = self.friend_repo.find_by_id(request_id)
        if not friendship:
            return False, "Friend request not found"

        # Verify that the current user is the recipient
        if friendship.friend_id != user_id:
            return False, "You cannot reject this friend request"

        # Verify it's pending
        if friendship.status != 'pending':
            return False, "This friend request is not pending"

        # Reject the request
        self.friend_repo.reject_friend_request(request_id)
        return True, "Friend request rejected"

    def get_pending_requests(self, user_id):
        """
        Get all pending friend requests for a user (received).
        Returns list of Friend objects with sender details.
        """
        pending_requests = self.friend_repo.get_pending_requests_received(user_id)

        # Enrich with user details
        enriched_requests = []
        for request in pending_requests:
            sender = self.user_repo.find_by_id(request.user_id)
            if sender:
                enriched_requests.append({
                    'request_id': request.id,
                    'from_user_id': request.user_id,
                    'from_email': sender.email,
                    'created_at': request.created_at.isoformat() if request.created_at else None
                })

        return enriched_requests

    def get_friends_list(self, user_id):
        return self.friend_repo.get_friends_list(user_id)
