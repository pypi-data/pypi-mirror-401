"""
Simple pass-through service for API keys.

Since AIDiscuss stores all data locally on the user's machine with no remote sync,
encryption is not necessary. API keys are stored as plain text in the local database.
"""


class EncryptionService:
    """
    Simple pass-through service that stores API keys as plain text.

    No encryption is used since all data stays local on the user's machine.
    """

    def encrypt(self, plaintext: str) -> str:
        """
        Return plaintext as-is (no encryption).

        Args:
            plaintext: The string to store

        Returns:
            The same string unchanged
        """
        return plaintext if plaintext else ""

    def decrypt(self, ciphertext: str) -> str:
        """
        Return text as-is (no decryption needed).

        Args:
            ciphertext: The string to retrieve

        Returns:
            The same string unchanged
        """
        return ciphertext if ciphertext else ""


# Global singleton instance
encryption_service = EncryptionService()
