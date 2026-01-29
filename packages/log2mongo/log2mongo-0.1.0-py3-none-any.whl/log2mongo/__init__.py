"""
log2mongo, it is a lightweight module for storing logs in MongoDB. To report any defects send an email: ablopego@gmail.com
"""
__version__ = "0.1.0"

__all__ = ["log2mongo"]

from log2mongo.mongo_logger import MongoLogger as log2mongo