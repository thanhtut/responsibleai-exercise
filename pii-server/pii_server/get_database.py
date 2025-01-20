from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from tiny_pii.types import TinyPIIOutput, TinyPIIDetection

Base = declarative_base()


# Database connection URL format:
# postgresql://username:password@host:port/database_name
DATABASE_URL = "postgresql://piiserver:TowardsFairAI@localhost:5432/piidatabase"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the base class for declarative models
Base = declarative_base()


class PIIAnalysisOutput(Base):
    __tablename__ = "pii_analyses"

    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    name = Column(Integer, nullable=False)
    email = Column(Integer, nullable=False)
    phone = Column(Integer, nullable=False)
    nric = Column(Integer, nullable=False)
    address = Column(Integer, nullable=False)
    detections = Column(JSON, nullable=False)
    redacted_text = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    @classmethod
    def from_pii_output(cls, pii_output: TinyPIIOutput):
        """
        Create a PIIAnalysis instance from a TinyPIIOutput object.
        """
        return cls(
            text=pii_output.text,
            name=pii_output.name,
            email=pii_output.email,
            phone=pii_output.phone,
            nric=pii_output.nric,
            address=pii_output.address,
            detections=[detection.dict() for detection in pii_output.detections],
            redacted_text=pii_output.redacted_text,
        )

    def to_pii_output(self) -> TinyPIIOutput:
        """
        Convert the database model back to a TinyPIIOutput object.
        """
        return TinyPIIOutput(
            text=self.text,
            name=self.name,
            email=self.email,
            phone=self.phone,
            nric=self.nric,
            address=self.address,
            detections=[TinyPIIDetection(**detection) for detection in self.detections],
            redacted_text=self.redacted_text,
        )


# Create all tables
Base.metadata.create_all(bind=engine)


# Function to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
