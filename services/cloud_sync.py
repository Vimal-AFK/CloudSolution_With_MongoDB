import socket
import time
import logging

logger = logging.getLogger(__name__)

class CloudSync:
    def __init__(self, local_db, cloud_db, sync_interval=5):
        self.local_db = local_db
        self.cloud_db = cloud_db
        self.sync_interval = sync_interval

    def is_cloud_available(self) -> bool:
        """
        Checks if the cloud database is reachable and functional.

        :return: True if the cloud is available, False otherwise.
        """
        try:
            # Test Internet connectivity
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            # Test cloud database connection
            self.cloud_db.client.admin.command('ping')
            return True
        except Exception as e:
            logger.warning(f"Cloud unavailable: {e}")
            return False

    def sync_to_cloud(self):
        """
        Continuously syncs local database items to the cloud database.
        Retries on failure and ensures robust logging.
        """
        while True:
            try:
                if self.is_cloud_available():
                    item = self.local_db.dequeue_data()
                    if item:
                        try:
                            self.cloud_db.enqueue_data(item)
                            logger.info(f"Successfully synced item to cloud: {item}")
                        except Exception as e:
                            logger.error(f"Failed to sync item to cloud: {e}")
                            self.local_db.enqueue_data(item)  # Requeue on failure
                    else:
                        logger.debug("No items in local queue to sync.")
                else:
                    logger.debug("Cloud not available. Skipping sync.")
            except Exception as e:
                logger.error(f"Unexpected error during sync: {e}")
            time.sleep(self.sync_interval)
