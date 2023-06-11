from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime


class UserBase(SQLModel):
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    username: str
    password: str
    face: Optional[bool] = Field(default=False)


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    results: List["Result"] = Relationship(back_populates="user")
    charts: List["Chart"] = Relationship(back_populates="user")


class UserRead(UserBase):
    id: int


class TestTypeBase(SQLModel):
    name: str


class TestType(TestTypeBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tests: List["Test"] = Relationship(back_populates="testType")


class TestTypeRead(TestTypeBase):
    id: int


class TopicBase(SQLModel):
    name: str


class Topic(TopicBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tests: List["Test"] = Relationship(back_populates="topic")


class TopicRead(TopicBase):
    id: int


class TestQuestionLink(SQLModel, table=True):
    testId: Optional[int] = Field(default=None, foreign_key="test.id", primary_key=True)
    questionId: Optional[int] = Field(default=None, foreign_key="question.id", primary_key=True)


class QuestionBase(SQLModel):
    description: str


class Question(QuestionBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tests: List["Test"] = Relationship(back_populates="questions", link_model=TestQuestionLink)
    choices: List["Choice"] = Relationship(back_populates="question")


class TestBase(SQLModel):
    name: str


class Test(TestBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    idTestType: int = Field(default=None, foreign_key="testtype.id")
    testType: TestType = Relationship(back_populates="tests")
    idTopic: int = Field(default=None, foreign_key="topic.id")
    topic: Topic = Relationship(back_populates="tests")
    questions: List["Question"] = Relationship(back_populates="tests", link_model=TestQuestionLink)
    charts: List["Chart"] = Relationship(back_populates="test")


class ChoiceBase(SQLModel):
    answer: str
    isTrue: bool = Field(default=False)


class Choice(ChoiceBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    idQuestion: int = Field(default=None, foreign_key="question.id")
    question: Question = Relationship(back_populates="choices")


class ChoiceRead(ChoiceBase):
    id: int


class QuestionRead(QuestionBase):
    id: int
    choices: List[ChoiceRead] = []


class TestReadContent(TestBase):
    id: int
    testType: TestTypeRead
    questions: List[QuestionRead] = []


class TestReadTitle(TestBase):
    id: int
    testType: TestTypeRead
    topic: TopicRead


class ResultBase(SQLModel):
    score: float
    date: datetime


class Result(ResultBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    idTest: Optional[int] = Field(default=None, foreign_key="test.id")
    test: Test = Relationship()
    idUser: Optional[int] = Field(default=None, foreign_key="user.id")
    user: User = Relationship(back_populates="results")


class ResultRead(ResultBase):
    id: int
    test: TestBase


class ChartTypeBase(SQLModel):
    name: str


class ChartType(ChartTypeBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    charts: List["Chart"] = Relationship(back_populates="chartType")


class ChartTypeRead(ChartTypeBase):
    id: int


class ChartBase(SQLModel):
    date: datetime


class Chart(ChartBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    idUser: Optional[int] = Field(default=None, foreign_key="user.id")
    user: User = Relationship(back_populates="charts")
    idTest: Optional[int] = Field(default=None, foreign_key="test.id")
    test: Test = Relationship(back_populates="charts")
    idChartType: Optional[int] = Field(default=None, foreign_key="charttype.id")
    chartType: ChartType = Relationship(back_populates="charts")
    captures: List["Capture"] = Relationship()


class EmotionBase(SQLModel):
    name: str


class Emotion(EmotionBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    captures: List["Capture"] = Relationship(back_populates="emotion")


class EmotionRead(EmotionBase):
    id: int


class CaptureBase(SQLModel):
    confidence: float


class Capture(CaptureBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    idChart: Optional[int] = Field(default=None, foreign_key="chart.id")
    chart: Chart = Relationship(back_populates="captures")
    idEmotion: Optional[int] = Field(default=None, foreign_key="emotion.id")
    emotion: Emotion = Relationship()
    angry: Optional[float] = None
    disgust: Optional[float] = None
    fear: Optional[float] = None
    happy: Optional[float] = None
    neutral: Optional[float] = None
    sad: Optional[float] = None
    surprise: Optional[float] = None
    proof: Optional[str] = None


class CaptureRead(CaptureBase):
    id: int
    emotion: EmotionRead


class ChartReadTable(ChartBase):
    id: int
    test: TestBase
    chartType: ChartTypeRead


class ChartRead(ChartBase):
    id: int
    captures: List[CaptureRead] = []
    test: TestBase


class FaceEmotionRequest(SQLModel):
    idUser: int
    idChart: int
    base64: str


class VoiceEmotionRequest(SQLModel):
    idUser: int
    idChart: int
    base64: str


class QuestionAnswer(SQLModel):
    questionId: int
    answerId: Optional[int] = None


class TestSheet(SQLModel):
    idTest: int
    idUser: int
    answers: List[QuestionAnswer] = []
