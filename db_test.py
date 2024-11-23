from sqlalchemy import Column, String, Integer, create_engine, select
from sqlalchemy.orm import declarative_base, Session, Mapped, mapped_column

Base = declarative_base()

class Headline(Base):
    __tablename__ = "headlines"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]= mapped_column(nullable=False)
    link: Mapped[str] = mapped_column()
    pub_date: Mapped[str] = mapped_column()  # todo: use datetime type for pubDate
    description: Mapped[str] = mapped_column()
    channel: Mapped[str] = mapped_column()  # todo: add channel table and foreign key

    def __repr__(self):
        return f"Headline(id={self.id}, title={self.title}, pub_date={self.pub_date})"

engine = create_engine("sqlite:///instance\db.sqlite")

headline1 = Headline(
    id=1,
    title="Die Grünen: Habeck will Kanzlerkandidat werden",
    link="https://www.sueddeutsche.de/politik/gruene-robert-habeck-kanzlerkandidatur-neuwahl-vertrauensfrage-lux.6A78n3DJ287L8yAksGte1E",
    pub_date="Fri, 08 Nov 2024 08:49:47 GMT",
    description="Der Wirtschaftsminister wird heute offiziell ankündigen, dass er sich als Spitzenkandidat der Grünen bewerben will. Überraschend kommt das nicht, aber in der Partei ist nicht jeder begeistert.",
    channel="sz",
    )
headline2 = Headline(
    id=2,
    title="Im Dienste Moskaus: Nord Stream 2 hätte wohl nie genehmigt werden dürfen",
    link="https://www.faz.net/aktuell/politik/inland/nord-stream-2-haette-wohl-nie-genehmigt-werden-duerfen-110096347.html",
    pub_date="Fri, 08 Nov 2024 07:58:01 +0100<",
    description="""<p><img width="190" height="107" border="0" title="Das Verlegeschiff &amp;quot;Audacia&amp;quot; des Offshore-Dienstleisters Allseas verlegt 2018 in der Ostsee vor der Insel Rügen Rohre für die Gaspipeline Nord Stream 2." alt="Das Verlegeschiff &amp;quot;Audacia&amp;quot; des Offshore-Dienstleisters Allseas verlegt 2018 in der Ostsee vor der Insel Rügen Rohre für die Gaspipeline Nord Stream 2." src="https://media0.faz.net/ppmedia/aktuell/4155922969/1.10098004/article_teaser/das-verlegeschiff-audacia-des.jpg" /></p><p>Die Zulassung für Nord Stream 2 hätte wohl nie erteilt werden dürfen. Das zeigen Dokumente, die der F.A.Z. vorliegen. Aber in Schwerin drückte man die Augen zu.</p>""",
    channel="sz",
    )

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

with Session(engine) as session:
    session.add(headline1)
    session.add(headline2)
    session.commit()

stmt = select(Headline)
with Session(engine) as session:
    headlines = session.execute(stmt)
    for h in headlines:
        print(h)
