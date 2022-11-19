class SignUp(Base):
    __tablename__ = "signup"
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(15), nullable=False)
    first_name = Column(String(30), nullable=False)
    last_name = Column(String(30), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String, nullable=False)
    image_url = Column(String(300))

class SignIn(Base):
    __tablename__ = "signin"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String, nullable=False)

class ChangePassword(Base):
    __tablename__ = "changepassword"
    id = Column(Integer, primary_key=True, nullable=False)
    oldpassword = Column(String(8),nullable=False)
    newpassword = Column(String(8), nullable=False)


class ForgotPassword(Base):
    __tablename__ = "forgot_password"
    id = Column(Integer, primary_key=True, nullable=False)
    


