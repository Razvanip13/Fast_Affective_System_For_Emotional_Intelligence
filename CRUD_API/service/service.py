from domain.models import User, Emotion, Test, Chart, Capture, TestSheet, Result
from sqlmodel import Session, select, and_
from typing import List
from datetime import datetime


class Service:

    def __init__(self):
        pass

    def get_user_by_id(self, session: Session, idUser: int) -> User:
        statement = select(User).where(User.id == idUser)
        result = session.exec(statement).first()

        return result

    def get_all_users(self, session: Session) -> List[User]:
        statement = select(User)
        results = session.exec(statement).all()

        return results

    def login_user(self, username: str, password: str, session: Session) -> User:
        statement = select(User).where(and_(User.username == username, User.password == password))
        result = session.exec(statement).first()

        return result

    def get_all_tests(self, session: Session, limit: int, offset: int) -> List[Test]:
        statement = select(Test).limit(limit).offset(offset)
        results = session.exec(statement).all()

        return results

    def get_all_emotions(self, session: Session) -> List[Emotion]:
        statement = select(Emotion)
        results = session.exec(statement).all()

        return results

    def get_all_charts(self, session: Session) -> List[Chart]:
        statement = select(Chart)
        results = session.exec(statement).all()

        return results

    def get_charts_for_user(self, id_user: int, session: Session) -> List[Chart]:
        statement = select(Chart).where(Chart.idUser == id_user)
        results = session.exec(statement).all()

        results.sort(key=lambda x: x.date, reverse=True)

        return results

    def get_chart(self, id_chart: int, session: Session) -> Chart:
        statement = select(Chart).where(Chart.id == id_chart)
        result = session.exec(statement).first()

        for i in range(len(result.captures)):
            result.captures[i].confidence = int(result.captures[i].confidence*100)

        return result

    def get_captures(self, session: Session) -> List[Capture]:
        statement = select(Capture)
        results = session.exec(statement).all()

        return results

    def get_test(self, user_id: int, session: Session) -> Test:
        statement = select(Test).where(Test.id == user_id)
        result = session.exec(statement).first()

        return result

    def evaluate_test(self, testSheet: TestSheet, session: Session):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        test = session.exec(select(Test).where(Test.id == testSheet.idTest)).first()
        score = 0

        for index, answer in enumerate(testSheet.answers):
            if answer.answerId is None:
                continue

            for question in test.questions:
                if question.id == answer.questionId:
                    for choice in question.choices:
                        if choice.id == answer.answerId:
                            if choice.isTrue:
                                score += 1
                            break
                    break

        score = float(score / len(testSheet.answers))

        result = Result(
            idTest=str(testSheet.idTest),
            idUser=str(testSheet.idUser),
            score=score,
            date=str(now)
        )

        session.add(result)
        session.commit()

    def get_user_results(self, idUser: int, session: Session) -> List[Result]:
        statement = select(Result).where(Result.idUser == idUser)
        results = session.exec(statement).all()

        for i in range(len(results)):
            results[i].score = int(results[i].score*100)
            results[i].date = results[i].date.strftime("%Y-%m-%d %H:%M:%S")

        results.sort(key=lambda x:x.date, reverse=True)

        return results

    def create_charts(self, idUser: int, idTest: int, session: Session) -> str:
        test = session.exec(select(Test).where(Test.id == idTest)).first()

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if test.testType.name == 'Oral':
            chart_face = Chart(
                idUser=str(idUser),
                idTest=str(idTest),
                idChartType=1,
                date=str(now)
            )

            session.add(chart_face)
            session.commit()
            session.refresh(chart_face)

            chart_voice = Chart(
                idUser=str(idUser),
                idTest=str(idTest),
                idChartType=2,
                date=str(now)
            )

            session.add(chart_voice)
            session.commit()
            session.refresh(chart_voice)

            return {'idChartFace': chart_face.id, 'idChartVoice': chart_voice.id}

        else:
            chart_face = Chart(
                idUser=str(idUser),
                idTest=str(idTest),
                idChartType=1,
                date=str(now)
            )

            session.add(chart_face)
            session.commit()
            session.refresh(chart_face)

            return {'idChartFace': chart_face.id}
