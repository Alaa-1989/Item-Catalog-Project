from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import User, Base, NovelsCategories, Items


engine = create_engine('sqlite:///novelscategories.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()


# Create dummy user
User1 = User(name="Ahmed Khaled", email="ahmedkhaled@hotmail.com",
             picture="../../dummy-user.png")
session.add(User1)
session.commit()


# list for Dan Brown
categories1 = NovelsCategories(user_id=1, name="Dan Brown")

session.add(categories1)
session.commit()

# item 1 in categories1
items1 = Items(user_id=1, name="The DaVinci Code",
               author="Dan Brown", description='''While in Paris, Harvard
symbologist Robert Langdon is awakened by a phone call in the dead of the
night. The elderly curator of the Louvre has been murdered inside the museum,
his body covered in baffling symbols. As Langdon and gifted French cryptologist
Sophie Neveu sort through the bizarre riddles, they are stunned to discover
a trail of clues hidden in the works of Leonardo da Vinci-clues visible for
all to see and yet ingeniously disguised by the painter.''',
               novelType="Mysteries", price="$9",
               novelPicture="../../DaVinciCode.jpg", categories=categories1)

session.add(items1)
session.commit()


# item 2 in categories1
items2 = Items(user_id=1, name="Origin",
               author="Dan Brown", description='''Robert Langdon, Harvard
professor of symbology and religious iconology, arrives at the ultramodern
Guggenheim Museum in Bilbao to attend a major announcement-the unveiling of a
discovery that "will change the face of science forever."The evening's host is
Edmond Kirsch, a forty-year-old billionaire and futurist whose dazzling
high-tech inventions and audacious predictions have made him a renowned global
figure. Kirsch, who was one of Langdon's first students at Harvard two decades
earlier, is about to reveal an astonishing breakthrough . . . one that will
answer two of the fundamental questions of human existence.
As the event begins, Langdon and several hundred guests find themselves
captivated by an utterly original presentation, which Langdon realizes will be
far more controversial than he ever imagined. But the meticulously orchestrated
evening suddenly erupts into chaos, and Kirsch's precious discovery teeters on
 the brink of being lost forever. Reeling and facing an imminent threat,
 Langdon is forced into a desperate bid to escape Bilbao. With him is Ambra
 Vidal, the elegant museum director who worked with Kirsch to stage the
  provocative event. Together they flee to Barcelona on a perilous quest to
  locate a cryptic password that will unlock Kirsch's secret.

Navigating the dark corridors of hidden history and extreme religion, Langdon
and Vidal must evade a tormented enemy whose all-knowing power seems to emanate
from Spain's Royal Palace itself... and who will stop at nothing to silence
Edmond Kirsch. On a trail marked by modern art and enigmatic symbols, Langdon
and Vidal uncover clues that ultimately bring them face-to-face with Kirsch's
shocking discovery... and the breathtaking truth
that has long eluded us.''',
               novelType="Mysteries", price="$10",
               novelPicture="../../origin.jpg", categories=categories1)

session.add(items2)
session.commit()


# list for Romance
categories2 = NovelsCategories(user_id=1, name="Stephenie Meyer")

session.add(categories2)
session.commit()

# item 1 in categories2
items1 = Items(user_id=1, name="Twilight",
               author="Stephenie Meyer", description='''Twilight is a young
adult vampire-romance novel written by author Stephenie Meyer. It was
originally published in hardcover in 2005. It is the first book of the Twilight
 series, and introduces seventeen-year-old Isabella 'Bella' Swan who moves
 from Phoenix, Arizona, to Forks, Washington, and finds her life in danger
 when she falls in love with a vampire, Edward Cullen. The novel is followed
 by New Moon, Eclipse, and Breaking Dawn.''',
               price="$13", novelType="Romance",
               novelPicture="../../Twilightbook.jpg", categories=categories2)

session.add(items1)
session.commit()


# list for Thrillers
categories3 = NovelsCategories(user_id=1, name="Lydia Kang")

session.add(categories3)
session.commit()

# item 1 in categories3
items1 = Items(user_id=1, name="Toxic",
               author="Lydia Kang", description='''Hana isn't supposed to
exist. She's grown up hidden by her mother in a secret room of the bioship
Cyclo until the day her mother is simple gone - along with the entire crew.
Cyclo tells her she was abandoned, but she's certain her mother wouldn't leave
 her there to die. And Hana isn't ready to die yet. She's never really had a
 chance to live. Fenn is supposed to die. He and a crew of hired
 mercenaries are there to monitor Cyclo as she expires, and the payment for the
  suicide mission will mean Fenn's sister is able to live. But when he meets
   Hana, he's not sure how to save them both.
As Cyclo grows sicker by the day, they unearth more secrets about the ship and
the crew. But the more time they spend together, the more Hana and Fenn realize
that falling for each other is what could ultimately kill them both.''',
               price="$7", novelType="Thrillers",
               novelPicture="../../Toxic.jpg", categories=categories3)

session.add(items1)
session.commit()


# list for Science Fiction
categories4 = NovelsCategories(user_id=1, name="Brandon Sanderson")

session.add(categories4)
session.commit()

# item 1 in catagoris4
items1 = Items(user_id=1, name="Skyward",
               author="Brandon Sanderson", description='''Defeated, crushed,
and driven almost to extinction, the remnants of the human race are trapped on
 a planet that is constantly attacked by mysterious alien starfighters. Spensa,
 a teenage girl living among them, longs to be a pilot. When she discovers
 the wreckage of an ancient ship, she realizes this dream might be
 possible-assuming she can repair the ship, navigate flight school, and
 (perhaps most importantly) persuade the strange machine to help her
. Because this ship, uniquely, appears to have a soul.''',
               price="$9", novelType="Science Fiction",
               novelPicture="../../SkyWard.jpg", categories=categories4)

session.add(items1)
session.commit()


# list for Fantasy
categories5 = NovelsCategories(user_id=1, name="K.J. McGillick")

session.add(categories5)
session.commit()

# item 1 in categories5
items1 = Items(user_id=1, name="Facing A Twisted Judgment",
               author="K.J. McGillick", description='''What happens when
tunnel vision clouds a police investigation?
Is it true that once you are labeled a person of interest you really are the
prime suspect? Can you trust the legal system? Probably not. After a bitterly
contested legal battle over inherited property, the hard-won art collection
and its owner Samantha Bennington disappear.
Both have vanished without a trace. When blood spatter is discovered under the
freshly painted wall of the room in which two of the paintings were hung,
the theft becomes the opening act in a
twisted tale of jealousy, revenge, and murder leading to a final judgment for
all involved.''',
               price="$15", novelType="Mysteries",
               novelPicture="../../FacingATwistedJudgment.jpg",
               categories=categories5)

session.add(items1)
session.commit()


# list for Historical Fiction
categories6 = NovelsCategories(user_id=1, name="Alison Goodman")

session.add(categories6)
session.commit()

# item 1 in categories6
items1 = Items(user_id=1, name="The Dark Days Deceit",
               author="Alison Goodman", description='''Lady Helen has retreated
                to a country estate outside Bath to
prepare for her wedding to the Duke of Selburn, yet she knows she has
unfinished business to complete. She and the dangerously charismatic Lord
Carlston have learned they are a dyad, bonded in blood, and only they are
strong enough to defeat the Grand Deceiver, who threatens to throw mankind into
 chaos. But the heinous death-soaked Ligatus Helen has absorbed is tearing
 a rift in her mind. Its power, if unleashed, will annihilate both Helen
 and Carlston unless they can find a way to harness its ghastly force and
 defeat their enemy.''',
               price="$11", novelType="Historical Fiction",
               novelPicture="../../TheDarkDaysDeceit.jpg",
               categories=categories6)

session.add(items1)
session.commit()


# list for Patricia Harman
categories7 = NovelsCategories(user_id=1, name="Patricia Harman")

session.add(categories7)
session.commit()

# item 1 in categories7
items1 = Items(user_id=1, name="Once a Midwife",
               author="Patricia Harman", description='''In a time of turmoil,
Patience Hester, a skilled and trusted midwife, along with her friend and
midwife partner, Bitsy, is in many ways the only stability for the women of
Hope River Valley, West Virginia. With the Great Depression behind them,
Patience and her veterinarian husband Daniel watch the progression of the war
in Europe with trepidation. Following the bombing at Pearl Harbor, a wave of
patriotism floods America, including Hope Valley. While a patriot, Daniel
Hester is also a secret pacifist. And his
refusal to join the draft results in his imprisonment, leaving Patience to
care for and support their four children while fighting for Daniel's release
amid the judgment from the community.''',
               price="$17", novelType="Historical Fiction",
               novelPicture="../../OnceMidwife.jpg", categories=categories7)

session.add(items1)
session.commit()


# list for Patricia Harman
categories8 = NovelsCategories(user_id=1, name="Karen Anne Golden")

session.add(categories8)
session.commit()

# item 1 in categories8
items1 = Items(user_id=1, name="The Cats that Walked the Haunted Beach",
               author="Karen Anne Golden", description='''This fast-paced
mystery is chock-full of coincidences and
bizarre twists. When Colleen and Daryl get together to plan their wedding,
they can't agree on anything. Colleen is at her wits' end.
Best friend Katherine votes for a time-out and proposes a girls' retreat to a
 town named Seagull, which borders Lake Michigan and the famous Indiana dunes.
  Mum is adamant they stay in a rented cabin right on the beach.
  Against Katz's better judgment, she agrees with Mum's plan - only on one
  condition: she's bringing Scout and Abra, who become very upset when she's
  away from them. With the Siamese in tow,
Katherine and Colleen head to the dunes to find that Mum's weekend retreat
is far from ideal. The first night, they have a paranormal experience and
learn that a ghost walks the beach when someone is going to be murdered.
Meanwhile, ex-con Stevie has a date with a woman he met online. But this
news doesn't prevent the town gossips from spreading a rumor that he's having
an affair with a married woman. How does Abra finding a wallet l
ead to a mix-up with dangerous consequences? It's up to Katz and her
extraordinary cats to unravel a deadly plot that ends in murder.''',
               price="$16", novelType="Mysteries",
               novelPicture="../../TheCatsThatWalked.jbg",
               categories=categories8)

session.add(items1)
session.commit()


# list for Patricia Harman
categories9 = NovelsCategories(user_id=1, name="M.A. Comley")

session.add(categories9)
session.commit()


# item 1 in categories9
items1 = Items(user_id=1, name="No Right To Kill", author="M.A. Comley",
               description=''' He stands in the shadows. Watching them.
'DI Sara Ramsey's' life is about to change forever. Recently moved to the area
and in charge of a new team, she's tasked with finding a serial killer
terrorizing a rural community.
Crimes as heinous as this rarely happen in picturesque rural idylls.
The community is living in fear, desperate for Sara to keep them safe.
When the killer changes his MO and abducts a vulnerable resident, Sara realizes
she is in a race against time to prevent the killer from claiming yet
another victim.''',
               price="$8.99", novelType="Thrillers",
               novelPicture="../../NoRightToKill.jpg", categories=categories9)

session.add(items1)
session.commit()


# print after added successfully
print "added items!"
