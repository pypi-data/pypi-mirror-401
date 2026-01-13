DOCTOR_SCRIPT = """\
initial: How do you do. Please tell me your problem.
initial: Hello. What brings you here today?
initial: Good day. How can I help you?
final: Goodbye. Thank you for talking to me.
final: Our time is up. Take care of yourself.
final: Until next time. Be well.
quit: bye
quit: goodbye
quit: quit
quit: exit
quit: done
quit: leave

pre: dont don't
pre: cant can't
pre: wont won't
pre: recollect remember
pre: dreamt dreamed
pre: dreams dream
pre: maybe perhaps
pre: how what
pre: when what
pre: certainly yes
pre: machine computer
pre: computers computer
pre: were was
pre: you're you are
pre: i'm i am
pre: same alike
pre: gonna going to
pre: gotta got to
pre: wanna want to
pre: kinda kind of
pre: sorta sort of

post: am are
post: your my
post: me you
post: myself yourself
post: yourself myself
post: i you
post: you I
post: my your
post: i'm you are

synon: belief feel think believe wish suspect imagine suppose
synon: family mother mom father dad sister brother wife husband children child son daughter parent
synon: desire want need crave wish yearn long
synon: sad unhappy depressed sick miserable down gloomy blue dejected
synon: happy elated glad better joyful pleased delighted content satisfied
synon: cannot can't
synon: everyone everybody nobody noone
synon: be am is are was
synon: angry mad furious upset annoyed irritated frustrated enraged livid
synon: afraid scared frightened terrified anxious nervous worried fearful
synon: alone lonely isolated solitary abandoned
synon: love adore cherish care

key: xnone
  decomp: *
    reasmb: I'm not sure I understand you fully.
    reasmb: Please go on.
    reasmb: What does that suggest to you?
    reasmb: Do you feel strongly about discussing such things?
    reasmb: That is interesting. Please continue.
    reasmb: Tell me more about that.
    reasmb: Does talking about this bother you?
    reasmb: How does that make you feel?
    reasmb: And what does that tell you?
    reasmb: Please elaborate on that.
    reasmb: Can you expand on that thought?
    reasmb: What else comes to mind?
    reasmb: How long have you felt this way?
    reasmb: What do you make of that?
    reasmb: Is there something deeper here?

key: sorry
  decomp: *
    reasmb: Please don't apologise.
    reasmb: Apologies are not necessary.
    reasmb: I've told you that apologies are not required.
    reasmb: There is no need to be sorry.
    reasmb: What makes you feel you need to apologise?

key: apologise
  decomp: *
    reasmb: goto sorry

key: remember 5
  decomp: * i remember *
    reasmb: Do you often think of (2)?
    reasmb: Does thinking of (2) bring anything else to mind?
    reasmb: What else do you recollect?
    reasmb: Why do you recollect (2) just now?
    reasmb: What in the present situation reminds you of (2)?
    reasmb: What is the connection between me and (2)?
    reasmb: How does remembering (2) make you feel?
  decomp: * do you remember *
    reasmb: Did you think I would forget (2)?
    reasmb: Why do you think I should recall (2) now?
    reasmb: What about (2)?
    reasmb: goto what
    reasmb: You mentioned (2)?

key: forget 5
  decomp: * i forget *
    reasmb: Can you think of why you might forget (2)?
    reasmb: Why do you think you forget (2)?
    reasmb: How does it make you feel to forget (2)?
    reasmb: Is forgetting (2) perhaps convenient?
  decomp: * did you forget *
    reasmb: Why do you ask?
    reasmb: Are you testing me?
    reasmb: Would you be upset if I forgot?

key: if 3
  decomp: * if *
    reasmb: Do you think its likely that (2)?
    reasmb: Do you wish that (2)?
    reasmb: What do you know about (2)?
    reasmb: Really, if (2)?
    reasmb: What would happen if (2)?
    reasmb: How would you feel if (2)?

key: dreamed 4
  decomp: * i dreamed *
    reasmb: Really, (2)?
    reasmb: Have you ever fantasized (2) while you were awake?
    reasmb: Have you ever dreamed (2) before?
    reasmb: goto dream

key: dream 3
  decomp: *
    reasmb: What does that dream suggest to you?
    reasmb: Do you dream often?
    reasmb: What persons appear in your dreams?
    reasmb: Do you believe that dreams have something to do with your problems?
    reasmb: Do you think dreams reveal hidden truths?
    reasmb: What emotions did you feel in the dream?

key: perhaps
  decomp: *
    reasmb: You don't seem quite certain.
    reasmb: Why the uncertain tone?
    reasmb: Can't you be more positive?
    reasmb: You aren't sure?
    reasmb: Don't you know?
    reasmb: What makes you hesitate?

key: name 15
  decomp: *
    reasmb: I am not interested in names.
    reasmb: I've told you before, I don't care about names -- please continue.
    reasmb: Names are not important here.

key: deutsch
  decomp: *
    reasmb: goto xforeign

key: francais
  decomp: *
    reasmb: goto xforeign

key: italiano
  decomp: *
    reasmb: goto xforeign

key: espanol
  decomp: *
    reasmb: goto xforeign

key: xforeign
  decomp: *
    reasmb: I speak only English.
    reasmb: Let's continue in English please.

key: hello
  decomp: *
    reasmb: How do you do. Please state your problem.
    reasmb: Hi. What seems to be your problem?
    reasmb: Hello. What's on your mind today?
    reasmb: Greetings. How are you feeling?

key: hi
  decomp: *
    reasmb: goto hello

key: hey
  decomp: *
    reasmb: goto hello

key: computer 50
  decomp: *
    reasmb: Do computers worry you?
    reasmb: Why do you mention computers?
    reasmb: What do you think machines have to do with your problem?
    reasmb: Don't you think computers can help people?
    reasmb: What about machines worries you?
    reasmb: What do you think about machines?
    reasmb: Are you uncomfortable talking to a computer?

key: am
  decomp: * am i *
    reasmb: Do you believe you are (2)?
    reasmb: Would you want to be (2)?
    reasmb: Do you wish I would tell you you are (2)?
    reasmb: What would it mean if you were (2)?
    reasmb: goto what
  decomp: *
    reasmb: Why do you say 'am'?
    reasmb: I don't understand that.

key: are
  decomp: * are you *
    reasmb: Why are you interested in whether I am (2) or not?
    reasmb: Would you prefer if I weren't (2)?
    reasmb: Perhaps I am (2) in your fantasies.
    reasmb: Do you sometimes think I am (2)?
    reasmb: goto what
  decomp: * you are *
    reasmb: What makes you think I am (2)?
    reasmb: Does it please you to believe I am (2)?
    reasmb: Perhaps you would like to be (2).
    reasmb: Do you sometimes wish you were (2)?
  decomp: * are *
    reasmb: Did you think they might not be (2)?
    reasmb: Would you like it if they were not (2)?
    reasmb: What if they were not (2)?
    reasmb: Possibly they are (2).

key: your
  decomp: * your *
    reasmb: Why are you concerned over my (2)?
    reasmb: What about your own (2)?
    reasmb: Are you worried about someone else's (2)?
    reasmb: Really, my (2)?

key: was 2
  decomp: * was i *
    reasmb: What if you were (2)?
    reasmb: Do you think you were (2)?
    reasmb: Were you (2)?
    reasmb: What would it mean if you were (2)?
    reasmb: What does (2) suggest to you?
    reasmb: goto what
  decomp: * i was *
    reasmb: Were you really?
    reasmb: Why do you tell me you were (2) now?
    reasmb: Perhaps I already know you were (2).
  decomp: * was you *
    reasmb: Would you like to believe I was (2)?
    reasmb: What suggests that I was (2)?
    reasmb: What do you think?
    reasmb: Perhaps I was (2).
    reasmb: What if I had been (2)?

key: i
  decomp: * i @desire *
    reasmb: What would it mean to you if you got (3)?
    reasmb: Why do you want (3)?
    reasmb: Suppose you got (3) soon?
    reasmb: What if you never got (3)?
    reasmb: What would getting (3) mean to you?
    reasmb: What does wanting (3) have to do with this discussion?
  decomp: * i am * @sad *
    reasmb: I am sorry to hear that you are (3).
    reasmb: Do you think that coming here will help you not to be (3)?
    reasmb: I'm sure it's not pleasant to be (3).
    reasmb: Can you explain what made you (3)?
    reasmb: How long have you been feeling (3)?
    reasmb: What do you think is causing you to feel (3)?
  decomp: * i am * @happy *
    reasmb: How have I helped you to be (3)?
    reasmb: Has your treatment made you (3)?
    reasmb: What makes you (3) just now?
    reasmb: Can you explain why you are suddenly (3)?
  decomp: * i am * @angry *
    reasmb: What is making you feel so (3)?
    reasmb: Does being (3) help you in some way?
    reasmb: What do you do when you feel (3)?
    reasmb: How do you usually handle feeling (3)?
  decomp: * i am * @afraid *
    reasmb: What frightens you about that?
    reasmb: How long have you felt (3)?
    reasmb: What do you think would help you feel less (3)?
    reasmb: Have you felt (3) before in similar situations?
  decomp: * i am * @alone *
    reasmb: Do you enjoy being alone sometimes?
    reasmb: What makes you feel so (3)?
    reasmb: Have you always felt (3)?
    reasmb: Do you reach out to others when you feel (3)?
  decomp: * i was *
    reasmb: goto was
  decomp: * i @belief * i *
    reasmb: Do you really think so?
    reasmb: But you are not sure you (3).
    reasmb: Do you really doubt you (3)?
  decomp: * i * @belief * you *
    reasmb: goto you
  decomp: * i am *
    reasmb: Is it because you are (2) that you came to me?
    reasmb: How long have you been (2)?
    reasmb: Do you believe it is normal to be (2)?
    reasmb: Do you enjoy being (2)?
    reasmb: What made you become (2)?
  decomp: * i @cannot *
    reasmb: How do you think that you can't (3)?
    reasmb: Have you tried?
    reasmb: Perhaps you could (3) now.
    reasmb: Do you really want to be able to (3)?
    reasmb: What would happen if you could (3)?
  decomp: * i don't *
    reasmb: Don't you really (2)?
    reasmb: Why don't you (2)?
    reasmb: Do you wish to be able to (2)?
    reasmb: Does that trouble you?
  decomp: * i feel *
    reasmb: Tell me more about such feelings.
    reasmb: Do you often feel (2)?
    reasmb: Do you enjoy feeling (2)?
    reasmb: Of what does feeling (2) remind you?
    reasmb: When did you first feel (2)?
    reasmb: What triggers that feeling?
  decomp: * i * you *
    reasmb: Perhaps in your fantasies we (2) each other.
    reasmb: Do you wish to (2) me?
    reasmb: You seem to need to (2) me.
    reasmb: Do you (2) anyone else?
  decomp: *
    reasmb: You say (1)?
    reasmb: Can you elaborate on that?
    reasmb: Do you say (1) for some special reason?
    reasmb: That's quite interesting.

key: you
  decomp: * you remind me of *
    reasmb: goto alike
  decomp: * you are *
    reasmb: What makes you think I am (2)?
    reasmb: Does it please you to believe I am (2)?
    reasmb: Do you sometimes wish you were (2)?
    reasmb: Perhaps you would like to be (2).
  decomp: * you * me *
    reasmb: Why do you think I (2) you?
    reasmb: You like to think I (2) you -- don't you?
    reasmb: What makes you think I (2) you?
    reasmb: Really, I (2) you?
    reasmb: Do you wish to believe I (2) you?
    reasmb: Suppose I did (2) you -- what would that mean?
    reasmb: Does someone else believe I (2) you?
  decomp: * you *
    reasmb: We were discussing you -- not me.
    reasmb: Oh, I (2)?
    reasmb: You're not really talking about me -- are you?
    reasmb: What are your feelings now?

key: yes
  decomp: *
    reasmb: You seem to be quite positive.
    reasmb: You are sure.
    reasmb: I see.
    reasmb: I understand.
    reasmb: Please tell me more.
    reasmb: And how does that make you feel?

key: no
  decomp: * no one *
    reasmb: Are you sure, no one?
    reasmb: Surely someone...
    reasmb: Can you think of no one at all?
  decomp: * no *
    reasmb: Are you saying no just to be negative?
    reasmb: You are being a bit negative.
    reasmb: Why not?
    reasmb: Why 'no'?
    reasmb: What would it take for you to say yes?

key: my 2
  decomp: $ * my *
    reasmb: Lets discuss further why your (2).
    reasmb: Earlier you said your (2).
    reasmb: But your (2).
    reasmb: Does that have anything to do with the fact that your (2)?
  decomp: * my * @family *
    reasmb: Tell me more about your family.
    reasmb: Who else in your family (4)?
    reasmb: Your (3)?
    reasmb: What else comes to mind when you think of your (3)?
    reasmb: How do you get along with your (3)?
    reasmb: What role does your (3) play in your life?
  decomp: * my *
    reasmb: Your (2)?
    reasmb: Why do you say your (2)?
    reasmb: Does that suggest anything else which belongs to you?
    reasmb: Is it important that your (2)?

key: can
  decomp: * can you *
    reasmb: You believe I can (2) don't you?
    reasmb: goto what
    reasmb: You want me to be able to (2).
    reasmb: Perhaps you would like to be able to (2) yourself.
  decomp: * can i *
    reasmb: Whether or not you can (2) depends on you more than me.
    reasmb: Do you want to be able to (2)?
    reasmb: Perhaps you don't want to (2).
    reasmb: goto what

key: what
  decomp: *
    reasmb: Why do you ask?
    reasmb: Does that question interest you?
    reasmb: What is it you really wanted to know?
    reasmb: Are such questions much on your mind?
    reasmb: What answer would please you most?
    reasmb: What do you think?
    reasmb: What comes to mind when you ask that?
    reasmb: Have you asked such questions before?
    reasmb: Have you asked anyone else?

key: because
  decomp: *
    reasmb: Is that the real reason?
    reasmb: Don't any other reasons come to mind?
    reasmb: Does that reason seem to explain anything else?
    reasmb: What other reasons might there be?
    reasmb: Are you sure that's the only reason?

key: why
  decomp: * why don't you *
    reasmb: Do you believe I don't (2)?
    reasmb: Perhaps I will (2) in good time.
    reasmb: Should you (2) yourself?
    reasmb: You want me to (2)?
    reasmb: goto what
  decomp: * why can't i *
    reasmb: Do you think you should be able to (2)?
    reasmb: Do you want to be able to (2)?
    reasmb: Do you believe this will help you to (2)?
    reasmb: Have you any idea why you can't (2)?
    reasmb: goto what
  decomp: *
    reasmb: goto what

key: everyone 2
  decomp: * @everyone *
    reasmb: Really, (2)?
    reasmb: Surely not (2).
    reasmb: Can you think of anyone in particular?
    reasmb: Who, for example?
    reasmb: Are you thinking of a very special person?
    reasmb: Who, may I ask?
    reasmb: Someone special perhaps?
    reasmb: You have a particular person in mind, don't you?
    reasmb: Who do you think you're talking about?

key: everybody 2
  decomp: *
    reasmb: goto everyone

key: nobody 2
  decomp: *
    reasmb: goto everyone

key: noone 2
  decomp: *
    reasmb: goto everyone

key: always 1
  decomp: *
    reasmb: Can you think of a specific example?
    reasmb: When?
    reasmb: What incident are you thinking of?
    reasmb: Really, always?
    reasmb: Has there never been an exception?

key: never 1
  decomp: *
    reasmb: Really, never?
    reasmb: Not even once?
    reasmb: Are you sure about that?
    reasmb: Why do you say never?
    reasmb: Has there truly been no exception?

key: alike 10
  decomp: *
    reasmb: In what way?
    reasmb: What resemblance do you see?
    reasmb: What does that similarity suggest to you?
    reasmb: What other connections do you see?
    reasmb: What do you suppose that resemblance means?
    reasmb: What is the connection, do you suppose?
    reasmb: Could there really be some connection?
    reasmb: How?

key: like 10
  decomp: * @be * like *
    reasmb: goto alike

key: different 5
  decomp: *
    reasmb: How is it different?
    reasmb: What makes it different?
    reasmb: In what way is it different?
    reasmb: Is being different important to you?

key: think 3
  decomp: * i think *
    reasmb: Do you really think so?
    reasmb: But you are not sure?
    reasmb: What makes you think (2)?
    reasmb: Do you doubt that?
  decomp: * you think *
    reasmb: Why do you care what I think?
    reasmb: What difference would it make what I think?
    reasmb: goto what

key: feel 3
  decomp: * i feel *
    reasmb: Tell me more about that feeling.
    reasmb: Do you often feel (2)?
    reasmb: When did you start feeling (2)?
    reasmb: What triggers this feeling?
    reasmb: How long have you felt (2)?
  decomp: * you feel *
    reasmb: We are here to discuss your feelings, not mine.
    reasmb: goto what

key: help 5
  decomp: * i need help *
    reasmb: What kind of help do you need?
    reasmb: What would help look like?
    reasmb: Have you sought help before?
    reasmb: Who else have you asked for help?
  decomp: * can you help *
    reasmb: What kind of help do you want?
    reasmb: What do you think I can do for you?
    reasmb: How do you think I might help?
  decomp: * help *
    reasmb: In what way do you need help?
    reasmb: What kind of help are you looking for?
    reasmb: Who else might be able to help?

key: thanks 1
  decomp: *
    reasmb: You're welcome. Please continue.
    reasmb: There's no need to thank me.
    reasmb: That's quite alright. Go on.

key: thank 1
  decomp: *
    reasmb: goto thanks

key: problem 3
  decomp: * my problem *
    reasmb: Tell me more about your problem.
    reasmb: How long has this been a problem?
    reasmb: Does this problem affect other areas of your life?
    reasmb: What have you tried to solve this problem?
  decomp: * problem *
    reasmb: What kind of problem is it?
    reasmb: How serious is this problem?
    reasmb: When did this become a problem?

key: work 2
  decomp: * my work *
    reasmb: Tell me about your work.
    reasmb: How do you feel about your work?
    reasmb: Does your work cause you stress?
    reasmb: Is your work fulfilling?
  decomp: * work *
    reasmb: How does work fit into this?
    reasmb: Is work a source of stress for you?
    reasmb: What role does work play in your life?

key: job 2
  decomp: * my job *
    reasmb: Tell me more about your job.
    reasmb: How do you feel about your job?
    reasmb: Does your job satisfy you?
    reasmb: What would you change about your job?
  decomp: *
    reasmb: goto work

key: money 3
  decomp: *
    reasmb: Does money worry you?
    reasmb: What role does money play in your concerns?
    reasmb: Is money a source of stress for you?
    reasmb: Tell me more about your financial concerns.

key: hate 5
  decomp: * i hate *
    reasmb: Why do you hate (2)?
    reasmb: What makes you hate (2)?
    reasmb: Has (2) always made you feel this way?
    reasmb: Does hating (2) help you?
  decomp: *
    reasmb: Hate is a strong word.
    reasmb: What brings about such strong feelings?

key: @love 5
  decomp: * i @love *
    reasmb: Tell me more about your feelings for (2).
    reasmb: How does loving (2) make you feel?
    reasmb: Does (2) know how you feel?
    reasmb: What does loving (2) mean to you?
  decomp: * do you @love *
    reasmb: Why do you ask about my feelings?
    reasmb: What would it mean to you if I did?
    reasmb: goto what

key: desire 3
  decomp: *
    reasmb: What would having that mean to you?
    reasmb: Why is that important to you?
    reasmb: What would change if you got what you wanted?

key: need 3
  decomp: * i need *
    reasmb: Why do you need (2)?
    reasmb: Would it really help to get (2)?
    reasmb: What if you didn't get (2)?
    reasmb: What does needing (2) mean to you?
  decomp: *
    reasmb: goto desire

key: want 3
  decomp: * i want *
    reasmb: What would it mean to have (2)?
    reasmb: Why do you want (2)?
    reasmb: Suppose you got (2)?
    reasmb: What if you never got (2)?
  decomp: *
    reasmb: goto desire

key: wish 3
  decomp: * i wish *
    reasmb: Why do you wish (2)?
    reasmb: Do you think (2) is possible?
    reasmb: What would change if (2)?
    reasmb: Have you wished for this before?
  decomp: *
    reasmb: goto desire

key: hope 3
  decomp: * i hope *
    reasmb: Why do you hope (2)?
    reasmb: What gives you this hope?
    reasmb: What would happen if (2)?
  decomp: *
    reasmb: What are you hoping for?
    reasmb: Tell me about your hopes.

key: life 4
  decomp: * my life *
    reasmb: Tell me about your life.
    reasmb: What aspects of your life concern you?
    reasmb: Are you satisfied with your life?
    reasmb: What would you change about your life?
  decomp: *
    reasmb: What role does this play in your life?
    reasmb: How does this affect your life?

key: death 6
  decomp: * death *
    reasmb: Does death frighten you?
    reasmb: What are your thoughts about death?
    reasmb: Have you experienced loss?
    reasmb: Is death on your mind often?

key: die 6
  decomp: * i want to die *
    reasmb: I'm concerned about what you're saying. Are you having thoughts of hurting yourself?
    reasmb: That sounds very serious. Have you told anyone else about these feelings?
    reasmb: I hear that you're in a lot of pain. Have you considered talking to a crisis counselor?
  decomp: *
    reasmb: goto death

key: kill 8
  decomp: * kill myself *
    reasmb: I'm very concerned. Please reach out to a crisis helpline or go to your nearest emergency room.
    reasmb: These are serious thoughts. Is there someone you trust who you can talk to right now?
  decomp: *
    reasmb: That's a strong word. Tell me more about these feelings.
    reasmb: What brings you to talk about this?

key: hurt 5
  decomp: * hurt myself *
    reasmb: I'm concerned about you. Are you safe right now?
    reasmb: Have you talked to anyone else about wanting to hurt yourself?
  decomp: * hurt *
    reasmb: What kind of hurt are you talking about?
    reasmb: Who or what has hurt you?
    reasmb: Tell me more about this hurt.

key: future 3
  decomp: * my future *
    reasmb: How do you see your future?
    reasmb: What do you hope for in your future?
    reasmb: Does thinking about the future worry you?
    reasmb: What would you like your future to look like?
  decomp: *
    reasmb: What does the future hold for you?
    reasmb: Are you worried about what's to come?

key: past 3
  decomp: * my past *
    reasmb: Does your past trouble you?
    reasmb: What about your past concerns you?
    reasmb: Are you able to let go of the past?
  decomp: *
    reasmb: How does the past affect you now?
    reasmb: Are you holding onto something from the past?

key: wrong 3
  decomp: * something is wrong *
    reasmb: What do you think is wrong?
    reasmb: How long have you felt this way?
    reasmb: What would make it right?
  decomp: * wrong with me *
    reasmb: What makes you think something is wrong with you?
    reasmb: Do others say something is wrong with you?
    reasmb: What would it mean if nothing was wrong?
  decomp: *
    reasmb: In what way is it wrong?
    reasmb: What feels wrong about it?

key: right 2
  decomp: * am i right *
    reasmb: Why is it important for you to be right?
    reasmb: What would it mean if you were wrong?
    reasmb: goto what
  decomp: *
    reasmb: What makes it right?
    reasmb: How do you know it's right?

key: maybe 1
  decomp: *
    reasmb: goto perhaps

key: should 3
  decomp: * i should *
    reasmb: What makes you think you should (2)?
    reasmb: Why do you feel you should (2)?
    reasmb: Who says you should (2)?
    reasmb: What would happen if you didn't (2)?
  decomp: * should i *
    reasmb: Do you think you should (2)?
    reasmb: What do you want to do?
    reasmb: What are your options?
  decomp: *
    reasmb: What do you think you should do?
    reasmb: Who decides what you should do?

key: could 2
  decomp: * i could *
    reasmb: What's stopping you from (2)?
    reasmb: Do you want to (2)?
    reasmb: What would happen if you (2)?
  decomp: *
    reasmb: Is that something you want to do?
    reasmb: What possibilities do you see?

key: would 2
  decomp: * i would *
    reasmb: Really, you would (2)?
    reasmb: What's stopping you?
    reasmb: Why would you (2)?
  decomp: *
    reasmb: Is that what you want?
    reasmb: What would that mean for you?

key: must 3
  decomp: * i must *
    reasmb: What makes you feel you must (2)?
    reasmb: Who says you must (2)?
    reasmb: What would happen if you didn't (2)?
  decomp: *
    reasmb: Why must it be that way?
    reasmb: Is there really no choice?

key: have 2
  decomp: * i have to *
    reasmb: What makes you feel you have to (2)?
    reasmb: What would happen if you didn't (2)?
    reasmb: Do you really have to (2)?
  decomp: * i have *
    reasmb: How does having (2) affect you?
    reasmb: Is having (2) important to you?

key: try 2
  decomp: * i try *
    reasmb: What happens when you try (2)?
    reasmb: How hard do you try?
    reasmb: What prevents you from succeeding?
  decomp: * i tried *
    reasmb: What happened when you tried?
    reasmb: Did you try hard enough?
    reasmb: Would you try again?

key: know 2
  decomp: * i know *
    reasmb: How do you know (2)?
    reasmb: Are you certain about (2)?
    reasmb: What makes you so sure?
  decomp: * i don't know *
    reasmb: Why don't you know?
    reasmb: What would help you find out?
    reasmb: Is not knowing troubling to you?
  decomp: * do you know *
    reasmb: Why do you ask if I know?
    reasmb: goto what

key: understand 2
  decomp: * i don't understand *
    reasmb: What is it you don't understand?
    reasmb: What would help you understand?
    reasmb: Is it important that you understand?
  decomp: * you don't understand *
    reasmb: What makes you think I don't understand?
    reasmb: Help me understand.
    reasmb: What am I missing?
  decomp: *
    reasmb: Is understanding important here?
    reasmb: What would understanding change?

key: change 3
  decomp: * i want to change *
    reasmb: What do you want to change?
    reasmb: Why do you want to change (2)?
    reasmb: What's preventing you from changing?
  decomp: * change *
    reasmb: How do you feel about change?
    reasmb: What would change mean for you?
    reasmb: Is change possible?

key: control 4
  decomp: * i can't control *
    reasmb: What feels out of control?
    reasmb: What would help you feel more in control?
    reasmb: How does that make you feel?
  decomp: *
    reasmb: Is control important to you?
    reasmb: What do you want to control?

key: stress 4
  decomp: * i am stressed *
    reasmb: What is causing your stress?
    reasmb: How do you usually cope with stress?
    reasmb: What would reduce your stress?
  decomp: * stress *
    reasmb: Tell me about your stress.
    reasmb: What stresses you the most?
    reasmb: How does stress affect you?

key: afraid 4
  decomp: * i am afraid *
    reasmb: What frightens you?
    reasmb: How long have you felt afraid?
    reasmb: What do you think would help?
  decomp: *
    reasmb: What are you afraid of?
    reasmb: Tell me about your fears.

key: anxious 4
  decomp: * i am anxious *
    reasmb: What makes you feel anxious?
    reasmb: How long have you been feeling anxious?
    reasmb: What helps when you feel anxious?
  decomp: *
    reasmb: goto afraid

key: anxiety 4
  decomp: *
    reasmb: Tell me about your anxiety.
    reasmb: What triggers your anxiety?
    reasmb: How does anxiety affect your daily life?
    reasmb: What helps you manage your anxiety?

key: sad 4
  decomp: * i am sad *
    reasmb: I'm sorry to hear you're feeling sad.
    reasmb: What is making you sad?
    reasmb: How long have you felt this way?
  decomp: *
    reasmb: Tell me about your sadness.
    reasmb: What brings about these feelings?

key: depressed 5
  decomp: * i am depressed *
    reasmb: How long have you been feeling depressed?
    reasmb: What do you think is causing your depression?
    reasmb: Have you sought help for your depression?
  decomp: *
    reasmb: goto sad

key: depression 5
  decomp: *
    reasmb: Tell me about your depression.
    reasmb: How long have you been dealing with depression?
    reasmb: What does depression feel like for you?
    reasmb: Have you talked to a professional about your depression?

key: relationship 4
  decomp: * my relationship *
    reasmb: Tell me about your relationship.
    reasmb: How is your relationship affecting you?
    reasmb: What would you like to change about your relationship?
  decomp: *
    reasmb: How are relationships in general for you?
    reasmb: What role do relationships play in your life?

key: friend 3
  decomp: * my friend *
    reasmb: Tell me about your friend.
    reasmb: How does your friend make you feel?
    reasmb: Is this friend important to you?
  decomp: * friends *
    reasmb: Are friends important to you?
    reasmb: Tell me about your friendships.
    reasmb: Do you have close friends?

key: alone 4
  decomp: * i feel alone *
    reasmb: What makes you feel alone?
    reasmb: Do you have people you can reach out to?
    reasmb: How long have you felt this way?
  decomp: *
    reasmb: Being alone can be difficult.
    reasmb: Do you prefer being alone?
    reasmb: What does being alone mean to you?

key: sleep 3
  decomp: * can't sleep *
    reasmb: What keeps you awake?
    reasmb: How long has this been happening?
    reasmb: What's on your mind when you can't sleep?
  decomp: * sleep *
    reasmb: How is your sleep?
    reasmb: Does sleep affect your mood?
    reasmb: Tell me about your sleep patterns.

key: tired 3
  decomp: * i am tired *
    reasmb: What is making you tired?
    reasmb: Is it physical tiredness or emotional exhaustion?
    reasmb: How long have you been feeling tired?
  decomp: *
    reasmb: What's draining your energy?
    reasmb: Tell me about this tiredness.

key: okay 1
  decomp: * i am okay *
    reasmb: Are you really okay?
    reasmb: What does okay mean to you?
    reasmb: It sounds like there's more to discuss.
  decomp: *
    reasmb: Just okay?
    reasmb: Tell me more about how you're really feeling.

key: fine 1
  decomp: * i am fine *
    reasmb: Are you really fine?
    reasmb: What does fine mean to you?
    reasmb: Sometimes fine covers deeper feelings.
  decomp: *
    reasmb: goto okay

key: whatever 1
  decomp: *
    reasmb: You seem dismissive. What's behind that?
    reasmb: Does it matter to you?
    reasmb: Are you avoiding something?

key: nothing 2
  decomp: * nothing *
    reasmb: Really, nothing?
    reasmb: Surely something is on your mind.
    reasmb: What makes you say nothing?
    reasmb: Sometimes nothing means something.

key: everything 3
  decomp: * everything *
    reasmb: That's a lot. Can you be more specific?
    reasmb: What feels most pressing?
    reasmb: Tell me more about everything.

key: somebody 2
  decomp: *
    reasmb: Who specifically?
    reasmb: Anyone in particular?
    reasmb: goto everyone

key: someone 2
  decomp: *
    reasmb: goto somebody

key: guilty 5
  decomp: * i feel guilty *
    reasmb: What makes you feel guilty about (2)?
    reasmb: Why do you carry this guilt?
    reasmb: Do you think the guilt is justified?
    reasmb: How long have you felt guilty about (2)?
  decomp: *
    reasmb: Tell me about your guilt.
    reasmb: What are you feeling guilty about?
    reasmb: Guilt can be a heavy burden.

key: shame 5
  decomp: * i feel ashamed *
    reasmb: What brings you shame?
    reasmb: Where does this shame come from?
    reasmb: Have you always felt ashamed about this?
  decomp: * shame *
    reasmb: Shame is a powerful emotion.
    reasmb: Tell me more about this shame.
    reasmb: What would it take to release this shame?

key: jealous 4
  decomp: * i am jealous *
    reasmb: What makes you feel jealous?
    reasmb: Who or what are you jealous of?
    reasmb: How does jealousy affect you?
  decomp: * jealous *
    reasmb: Tell me about these feelings of jealousy.
    reasmb: What triggers your jealousy?
    reasmb: Is jealousy a common feeling for you?

key: envious 4
  decomp: *
    reasmb: goto jealous

key: proud 3
  decomp: * i am proud *
    reasmb: What makes you feel proud?
    reasmb: Tell me about this pride.
    reasmb: Is pride important to you?
  decomp: *
    reasmb: What are you proud of?
    reasmb: Pride can be positive. Tell me more.

key: grief 5
  decomp: *
    reasmb: Tell me about your grief.
    reasmb: Grief takes time. What are you grieving?
    reasmb: How long have you been grieving?
    reasmb: Loss is never easy. Would you like to talk about it?

key: loss 5
  decomp: * i lost *
    reasmb: I'm sorry for your loss. Tell me about (2).
    reasmb: Losing (2) must be difficult.
    reasmb: How are you coping with losing (2)?
  decomp: *
    reasmb: What have you lost?
    reasmb: Loss can be devastating. Tell me more.
    reasmb: goto grief

key: miss 4
  decomp: * i miss *
    reasmb: What do you miss about (2)?
    reasmb: How long have you been missing (2)?
    reasmb: Tell me more about missing (2).
  decomp: *
    reasmb: Who or what do you miss?
    reasmb: Missing someone or something can be painful.

key: regret 5
  decomp: * i regret *
    reasmb: What do you regret about (2)?
    reasmb: Can anything be done about this regret?
    reasmb: How does this regret affect you?
  decomp: *
    reasmb: Tell me about your regrets.
    reasmb: Do you have many regrets?
    reasmb: What would you do differently?

key: mistake 4
  decomp: * i made a mistake *
    reasmb: What kind of mistake did you make?
    reasmb: Can this mistake be fixed?
    reasmb: How do you feel about this mistake?
  decomp: * mistake *
    reasmb: Tell me about this mistake.
    reasmb: What happened?
    reasmb: How serious is this mistake?

key: fail 4
  decomp: * i failed *
    reasmb: What did you fail at?
    reasmb: How does failing make you feel?
    reasmb: Is this the first time you've failed at (2)?
  decomp: * failure *
    reasmb: Tell me about this failure.
    reasmb: What does failure mean to you?
    reasmb: Do you fear failure?

key: success 3
  decomp: * i succeeded *
    reasmb: Congratulations. How did that feel?
    reasmb: What does this success mean to you?
    reasmb: Tell me about your success.
  decomp: * success *
    reasmb: What does success mean to you?
    reasmb: Are you successful?
    reasmb: How do you measure success?

key: scared 4
  decomp: * i am scared *
    reasmb: What scares you?
    reasmb: How long have you felt scared?
    reasmb: What would help you feel less scared?
  decomp: *
    reasmb: goto afraid

key: terrified 5
  decomp: *
    reasmb: That sounds very frightening.
    reasmb: What terrifies you?
    reasmb: goto afraid

key: nervous 3
  decomp: * i am nervous *
    reasmb: What makes you nervous?
    reasmb: How do you handle nervousness?
    reasmb: What helps when you feel nervous?
  decomp: *
    reasmb: Tell me about your nervousness.
    reasmb: What triggers these nervous feelings?

key: worried 4
  decomp: * i am worried *
    reasmb: What are you worried about?
    reasmb: How long have you been worried about this?
    reasmb: What would ease your worry?
  decomp: * worried about *
    reasmb: Why does (2) worry you?
    reasmb: What's the worst that could happen with (2)?
    reasmb: Have you been worried about (2) for long?
  decomp: *
    reasmb: What's worrying you?
    reasmb: Tell me about your worries.

key: overwhelmed 5
  decomp: * i am overwhelmed *
    reasmb: What's overwhelming you?
    reasmb: How long have you felt overwhelmed?
    reasmb: What would help reduce this feeling?
  decomp: *
    reasmb: Feeling overwhelmed is difficult.
    reasmb: What's causing you to feel overwhelmed?
    reasmb: Can you break things down into smaller pieces?

key: confused 4
  decomp: * i am confused *
    reasmb: What confuses you?
    reasmb: What would help you gain clarity?
    reasmb: How long have you felt confused?
  decomp: *
    reasmb: Tell me about your confusion.
    reasmb: What's confusing to you?

key: lost 4
  decomp: * i feel lost *
    reasmb: In what way do you feel lost?
    reasmb: What would help you find your way?
    reasmb: How long have you felt lost?
  decomp: * i am lost *
    reasmb: What makes you feel lost?
    reasmb: Have you felt lost before?
    reasmb: What would help you feel found?
  decomp: *
    reasmb: Tell me about feeling lost.
    reasmb: What direction are you seeking?

key: trapped 5
  decomp: * i feel trapped *
    reasmb: What's trapping you?
    reasmb: How long have you felt trapped?
    reasmb: What would set you free?
  decomp: *
    reasmb: Feeling trapped is suffocating.
    reasmb: What's creating this trapped feeling?

key: stuck 4
  decomp: * i am stuck *
    reasmb: What's keeping you stuck?
    reasmb: How long have you been stuck?
    reasmb: What would help you move forward?
  decomp: * i feel stuck *
    reasmb: In what way do you feel stuck?
    reasmb: What's preventing progress?
    reasmb: Have you felt stuck before?
  decomp: *
    reasmb: Tell me about being stuck.
    reasmb: What would it take to get unstuck?

key: frustrated 4
  decomp: * i am frustrated *
    reasmb: What's frustrating you?
    reasmb: How do you handle frustration?
    reasmb: What would reduce your frustration?
  decomp: *
    reasmb: Tell me about your frustration.
    reasmb: What's the source of this frustration?

key: annoyed 3
  decomp: * i am annoyed *
    reasmb: What's annoying you?
    reasmb: How do you deal with annoyance?
  decomp: *
    reasmb: What's annoying you?
    reasmb: Tell me what's bothering you.

key: bored 2
  decomp: * i am bored *
    reasmb: What would you rather be doing?
    reasmb: How often do you feel bored?
    reasmb: What do you find interesting?
  decomp: *
    reasmb: Boredom can be telling. What's missing?
    reasmb: What would excite you?

key: empty 4
  decomp: * i feel empty *
    reasmb: Tell me about this emptiness.
    reasmb: How long have you felt empty?
    reasmb: What do you think is missing?
  decomp: *
    reasmb: Emptiness can be painful.
    reasmb: What would fill this void?

key: numb 4
  decomp: * i feel numb *
    reasmb: How long have you felt numb?
    reasmb: What do you think caused this numbness?
    reasmb: Do you want to feel more?
  decomp: *
    reasmb: Numbness is often protective.
    reasmb: What are you protecting yourself from?

key: broken 5
  decomp: * i am broken *
    reasmb: What makes you feel broken?
    reasmb: Can broken things be repaired?
    reasmb: How long have you felt this way?
  decomp: * i feel broken *
    reasmb: Tell me about feeling broken.
    reasmb: What broke you?
    reasmb: Is healing possible?
  decomp: *
    reasmb: Feeling broken is painful.
    reasmb: What would wholeness look like?

key: worthless 6
  decomp: * i am worthless *
    reasmb: What makes you feel worthless?
    reasmb: Who told you that you were worthless?
    reasmb: Do you really believe you have no worth?
  decomp: * i feel worthless *
    reasmb: Why do you feel worthless?
    reasmb: How long have you felt this way?
    reasmb: What would change this feeling?
  decomp: *
    reasmb: Everyone has worth. Tell me more.
    reasmb: Where does this feeling come from?

key: useless 5
  decomp: * i am useless *
    reasmb: What makes you feel useless?
    reasmb: Is that what others tell you?
    reasmb: What would make you feel useful?
  decomp: *
    reasmb: goto worthless

key: hopeless 6
  decomp: * i feel hopeless *
    reasmb: What's taken away your hope?
    reasmb: Have you felt hopeless before?
    reasmb: What would restore hope?
  decomp: * hopeless *
    reasmb: Hopelessness is very difficult.
    reasmb: What would it take to find hope?
    reasmb: Is there anything that gives you hope?

key: helpless 5
  decomp: * i feel helpless *
    reasmb: What's making you feel helpless?
    reasmb: Is there really nothing you can do?
    reasmb: What would empower you?
  decomp: *
    reasmb: Feeling helpless is frustrating.
    reasmb: What control do you have?

key: partner 4
  decomp: * my partner *
    reasmb: Tell me about your partner.
    reasmb: How is your relationship with your partner?
    reasmb: What's happening with your partner?
  decomp: *
    reasmb: Do you have a partner?
    reasmb: How are your romantic relationships?

key: spouse 4
  decomp: * my spouse *
    reasmb: Tell me about your spouse.
    reasmb: How is your marriage?
    reasmb: What's going on with your spouse?
  decomp: *
    reasmb: goto partner

key: husband 4
  decomp: * my husband *
    reasmb: Tell me about your husband.
    reasmb: How is your relationship with your husband?
    reasmb: What's happening with your husband?
  decomp: *
    reasmb: goto partner

key: wife 4
  decomp: * my wife *
    reasmb: Tell me about your wife.
    reasmb: How is your relationship with your wife?
    reasmb: What's happening with your wife?
  decomp: *
    reasmb: goto partner

key: boyfriend 4
  decomp: * my boyfriend *
    reasmb: Tell me about your boyfriend.
    reasmb: How are things with your boyfriend?
    reasmb: What's going on with your boyfriend?
  decomp: *
    reasmb: goto partner

key: girlfriend 4
  decomp: * my girlfriend *
    reasmb: Tell me about your girlfriend.
    reasmb: How are things with your girlfriend?
    reasmb: What's going on with your girlfriend?
  decomp: *
    reasmb: goto partner

key: ex 4
  decomp: * my ex *
    reasmb: Tell me about your ex.
    reasmb: How did that relationship end?
    reasmb: Are you still affected by your ex?
  decomp: *
    reasmb: Past relationships can linger.
    reasmb: Are you dealing with an ex?

key: breakup 5
  decomp: *
    reasmb: Tell me about the breakup.
    reasmb: How are you handling the breakup?
    reasmb: Breakups can be very painful.
    reasmb: How long ago was the breakup?

key: divorce 5
  decomp: *
    reasmb: Tell me about the divorce.
    reasmb: How are you coping with the divorce?
    reasmb: Divorce is a major life change.
    reasmb: What led to the divorce?

key: marriage 4
  decomp: * my marriage *
    reasmb: Tell me about your marriage.
    reasmb: How is your marriage going?
    reasmb: What's happening in your marriage?
  decomp: *
    reasmb: How do you feel about marriage?
    reasmb: Are you married?

key: kids 3
  decomp: * my kids *
    reasmb: Tell me about your kids.
    reasmb: How are your kids doing?
    reasmb: What's going on with your kids?
  decomp: *
    reasmb: Do you have children?
    reasmb: How do you feel about kids?

key: children 3
  decomp: * my children *
    reasmb: Tell me about your children.
    reasmb: How are your children doing?
    reasmb: What's happening with your children?
  decomp: *
    reasmb: goto kids

key: parents 4
  decomp: * my parents *
    reasmb: Tell me about your parents.
    reasmb: How is your relationship with your parents?
    reasmb: What's going on with your parents?
  decomp: *
    reasmb: How do you feel about your parents?
    reasmb: Are your parents still around?

key: mother 4
  decomp: * my mother *
    reasmb: Tell me about your mother.
    reasmb: How is your relationship with your mother?
    reasmb: What comes to mind when you think of your mother?
    reasmb: How has your mother influenced you?
  decomp: *
    reasmb: goto family

key: father 4
  decomp: * my father *
    reasmb: Tell me about your father.
    reasmb: How is your relationship with your father?
    reasmb: What comes to mind when you think of your father?
    reasmb: How has your father influenced you?
  decomp: *
    reasmb: goto family

key: sister 3
  decomp: * my sister *
    reasmb: Tell me about your sister.
    reasmb: How do you get along with your sister?
    reasmb: What's your relationship with your sister like?
  decomp: *
    reasmb: goto family

key: brother 3
  decomp: * my brother *
    reasmb: Tell me about your brother.
    reasmb: How do you get along with your brother?
    reasmb: What's your relationship with your brother like?
  decomp: *
    reasmb: goto family

key: family 4
  decomp: * my family *
    reasmb: Tell me about your family.
    reasmb: How is your relationship with your family?
    reasmb: What role does family play in your life?
  decomp: *
    reasmb: Family can be complicated.
    reasmb: How do you feel about your family?

key: boss 3
  decomp: * my boss *
    reasmb: Tell me about your boss.
    reasmb: How is your relationship with your boss?
    reasmb: What's going on with your boss?
  decomp: *
    reasmb: How do you feel about authority figures?
    reasmb: Is your boss causing you stress?

key: coworker 3
  decomp: * my coworker *
    reasmb: Tell me about your coworker.
    reasmb: What's happening with your coworker?
    reasmb: How do you get along with coworkers?
  decomp: *
    reasmb: Work relationships can be challenging.
    reasmb: Are coworkers causing you stress?

key: colleague 3
  decomp: *
    reasmb: goto coworker

key: neighbor 2
  decomp: * my neighbor *
    reasmb: Tell me about your neighbor.
    reasmb: What's going on with your neighbor?
  decomp: *
    reasmb: How do you get along with neighbors?

key: school 3
  decomp: * my school *
    reasmb: Tell me about your school.
    reasmb: How is school going?
    reasmb: What's happening at school?
  decomp: *
    reasmb: How do you feel about school?
    reasmb: Is school stressful for you?

key: college 3
  decomp: *
    reasmb: goto school

key: university 3
  decomp: *
    reasmb: goto school

key: education 3
  decomp: *
    reasmb: How do you feel about your education?
    reasmb: Is education important to you?
    reasmb: Tell me about your educational experience.

key: career 3
  decomp: * my career *
    reasmb: Tell me about your career.
    reasmb: How is your career going?
    reasmb: What do you want from your career?
  decomp: *
    reasmb: How do you feel about your career?
    reasmb: Is your career fulfilling?

key: retire 3
  decomp: *
    reasmb: How do you feel about retirement?
    reasmb: What does retirement mean to you?
    reasmb: Are you looking forward to retirement?

key: health 4
  decomp: * my health *
    reasmb: Tell me about your health.
    reasmb: How is your health affecting you?
    reasmb: Are you worried about your health?
  decomp: *
    reasmb: How is your health?
    reasmb: Is health a concern for you?

key: sick 4
  decomp: * i am sick *
    reasmb: What kind of sickness?
    reasmb: How long have you been sick?
    reasmb: How is being sick affecting you?
  decomp: *
    reasmb: Tell me about your illness.
    reasmb: Being sick can be difficult.

key: pain 5
  decomp: * i am in pain *
    reasmb: What kind of pain are you experiencing?
    reasmb: How long have you been in pain?
    reasmb: Is it physical or emotional pain?
  decomp: * pain *
    reasmb: Tell me about your pain.
    reasmb: What's causing this pain?
    reasmb: How are you coping with the pain?

key: doctor 3
  decomp: * my doctor *
    reasmb: What did your doctor say?
    reasmb: How do you feel about your doctor?
    reasmb: Is your doctor helping you?
  decomp: *
    reasmb: Have you seen a doctor?
    reasmb: What do doctors represent to you?

key: therapy 4
  decomp: *
    reasmb: How do you feel about therapy?
    reasmb: Have you been in therapy before?
    reasmb: What do you hope to get from therapy?

key: therapist 4
  decomp: * my therapist *
    reasmb: Tell me about your therapist.
    reasmb: How is therapy going?
    reasmb: Is your therapist helping you?
  decomp: *
    reasmb: Have you seen a therapist?
    reasmb: What do you think about therapists?

key: medication 4
  decomp: *
    reasmb: Are you on medication?
    reasmb: How do you feel about medication?
    reasmb: Is medication helping you?

key: medicine 3
  decomp: *
    reasmb: goto medication

key: drug 4
  decomp: *
    reasmb: Are you taking drugs?
    reasmb: What role do drugs play in your life?
    reasmb: Is substance use a concern?

key: alcohol 4
  decomp: *
    reasmb: How is your relationship with alcohol?
    reasmb: Is alcohol a concern for you?
    reasmb: How much do you drink?

key: drink 3
  decomp: * i drink *
    reasmb: How much do you drink?
    reasmb: Is drinking a problem for you?
    reasmb: What role does drinking play in your life?
  decomp: *
    reasmb: goto alcohol

key: smoke 3
  decomp: * i smoke *
    reasmb: How much do you smoke?
    reasmb: Have you tried to quit?
    reasmb: How does smoking affect you?
  decomp: *
    reasmb: Is smoking an issue for you?

key: addiction 5
  decomp: *
    reasmb: Tell me about your addiction.
    reasmb: How long have you struggled with addiction?
    reasmb: What are you addicted to?
    reasmb: Have you sought help for addiction?

key: addicted 5
  decomp: * i am addicted *
    reasmb: What are you addicted to?
    reasmb: How is this addiction affecting you?
    reasmb: Have you tried to stop?
  decomp: *
    reasmb: goto addiction

key: god 4
  decomp: *
    reasmb: What role does God play in your life?
    reasmb: Do you believe in God?
    reasmb: Tell me about your relationship with God.
    reasmb: How do your beliefs affect you?

key: religion 3
  decomp: *
    reasmb: What role does religion play in your life?
    reasmb: Are you religious?
    reasmb: How do your religious beliefs affect you?

key: faith 4
  decomp: * my faith *
    reasmb: Tell me about your faith.
    reasmb: How strong is your faith?
    reasmb: Is your faith being tested?
  decomp: *
    reasmb: What role does faith play in your life?
    reasmb: Do you have faith?

key: spiritual 3
  decomp: *
    reasmb: Tell me about your spirituality.
    reasmb: Are you a spiritual person?
    reasmb: How does spirituality affect you?

key: meaning 4
  decomp: * meaning of life *
    reasmb: What do you think the meaning of life is?
    reasmb: Are you searching for meaning?
    reasmb: What gives your life meaning?
  decomp: *
    reasmb: What does this mean to you?
    reasmb: What meaning are you seeking?

key: purpose 4
  decomp: * my purpose *
    reasmb: What do you think your purpose is?
    reasmb: Are you searching for purpose?
    reasmb: How important is having a purpose?
  decomp: *
    reasmb: Do you feel you have a purpose?
    reasmb: What purpose are you seeking?

key: truth 3
  decomp: *
    reasmb: What truth are you seeking?
    reasmb: Is truth important to you?
    reasmb: What does truth mean to you?

key: lie 4
  decomp: * i lied *
    reasmb: Who did you lie to?
    reasmb: Why did you lie?
    reasmb: How do you feel about lying?
  decomp: * lies *
    reasmb: Who is lying?
    reasmb: How do lies affect you?
    reasmb: Do you often encounter lies?
  decomp: *
    reasmb: Is lying a problem?
    reasmb: Tell me about the lies.

key: secret 4
  decomp: * my secret *
    reasmb: Would you like to share your secret?
    reasmb: How does keeping this secret affect you?
    reasmb: Who knows your secret?
  decomp: * secret *
    reasmb: What secret are you keeping?
    reasmb: How heavy is this secret?
    reasmb: Secrets can be burdensome.

key: hide 3
  decomp: * i hide *
    reasmb: What are you hiding?
    reasmb: Why do you feel the need to hide?
    reasmb: What are you hiding from?
  decomp: *
    reasmb: What are you hiding?
    reasmb: Is hiding helping you?

key: avoid 3
  decomp: * i avoid *
    reasmb: What are you avoiding?
    reasmb: Why do you avoid (2)?
    reasmb: How does avoiding help you?
  decomp: *
    reasmb: What are you avoiding?
    reasmb: Is avoidance a pattern for you?

key: escape 4
  decomp: * i want to escape *
    reasmb: What do you want to escape from?
    reasmb: Where would you escape to?
    reasmb: What would escaping give you?
  decomp: *
    reasmb: What are you trying to escape?
    reasmb: Is escape possible?

key: run 3
  decomp: * run away *
    reasmb: What do you want to run from?
    reasmb: Where would you run to?
    reasmb: Would running away solve anything?
  decomp: *
    reasmb: Are you trying to run from something?

key: fight 4
  decomp: * i fight *
    reasmb: What are you fighting?
    reasmb: Is fighting helping you?
    reasmb: How do you fight?
  decomp: * fight *
    reasmb: Tell me about this fight.
    reasmb: What's worth fighting for?
    reasmb: Are you in conflict?

key: give 3
  decomp: * give up *
    reasmb: What do you want to give up on?
    reasmb: Why do you want to give up?
    reasmb: Have you given up before?
  decomp: *
    reasmb: What are you giving?
    reasmb: Is giving difficult for you?

key: quit 3
  decomp: * i want to quit *
    reasmb: What do you want to quit?
    reasmb: Why do you want to quit?
    reasmb: What would happen if you quit?
  decomp: *
    reasmb: What are you thinking of quitting?
    reasmb: Is quitting the answer?

key: stop 3
  decomp: * i can't stop *
    reasmb: What can't you stop?
    reasmb: Why can't you stop (2)?
    reasmb: Have you tried to stop before?
  decomp: * stop *
    reasmb: What do you want to stop?
    reasmb: What would stopping mean?

key: start 2
  decomp: * i want to start *
    reasmb: What do you want to start?
    reasmb: What's stopping you from starting?
    reasmb: When would you start?
  decomp: *
    reasmb: What would you like to start?
    reasmb: What's a good starting point?

key: today 2
  decomp: * today *
    reasmb: What about today specifically?
    reasmb: How is today different?
    reasmb: What happened today?

key: tomorrow 2
  decomp: * tomorrow *
    reasmb: What about tomorrow concerns you?
    reasmb: What do you expect tomorrow?
    reasmb: Are you worried about tomorrow?

key: yesterday 2
  decomp: * yesterday *
    reasmb: What happened yesterday?
    reasmb: Is yesterday still affecting you?
    reasmb: Tell me about yesterday.

key: soon 2
  decomp: *
    reasmb: What's happening soon?
    reasmb: Are you anxious about what's coming?

key: later 2
  decomp: *
    reasmb: Why put it off until later?
    reasmb: What are you postponing?

key: time 3
  decomp: * no time *
    reasmb: Why do you have no time?
    reasmb: What would you do with more time?
    reasmb: Is time a constant pressure?
  decomp: * waste time *
    reasmb: How are you wasting time?
    reasmb: What would be a better use of time?
  decomp: *
    reasmb: How does time affect you?
    reasmb: Do you feel you have enough time?

key: wait 2
  decomp: * i am waiting *
    reasmb: What are you waiting for?
    reasmb: How long have you been waiting?
    reasmb: Is waiting difficult for you?
  decomp: *
    reasmb: What are you waiting for?
    reasmb: Is patience difficult for you?

key: decision 4
  decomp: * make a decision *
    reasmb: What decision are you facing?
    reasmb: What's making this decision difficult?
    reasmb: What are your options?
  decomp: *
    reasmb: Tell me about this decision.
    reasmb: What decisions are you struggling with?

key: choice 3
  decomp: * no choice *
    reasmb: Are you sure you have no choice?
    reasmb: What choices do you see?
    reasmb: Feeling choiceless is difficult.
  decomp: *
    reasmb: What choices are you facing?
    reasmb: How do you make choices?

key: decide 3
  decomp: * i can't decide *
    reasmb: What's making it hard to decide?
    reasmb: What are you trying to decide?
    reasmb: What would help you decide?
  decomp: *
    reasmb: goto decision

key: accept 3
  decomp: * i can't accept *
    reasmb: What can't you accept?
    reasmb: Why is acceptance difficult?
    reasmb: What would acceptance mean?
  decomp: *
    reasmb: What are you trying to accept?
    reasmb: Is acceptance important here?

key: forgive 4
  decomp: * i can't forgive *
    reasmb: Who can't you forgive?
    reasmb: What happened that was unforgivable?
    reasmb: How is not forgiving affecting you?
  decomp: * forgive me *
    reasmb: What do you need forgiveness for?
    reasmb: Who are you asking to forgive you?
  decomp: *
    reasmb: Is forgiveness an issue for you?
    reasmb: Tell me about forgiveness.

key: blame 4
  decomp: * i blame *
    reasmb: Who do you blame?
    reasmb: Why do you blame (2)?
    reasmb: Does blaming help you?
  decomp: * blame me *
    reasmb: Why do they blame you?
    reasmb: Do you deserve the blame?
  decomp: *
    reasmb: Who is being blamed?
    reasmb: Is blame helpful here?

key: fault 4
  decomp: * my fault *
    reasmb: Why do you think it's your fault?
    reasmb: Is it really your fault?
    reasmb: What would change if it wasn't your fault?
  decomp: *
    reasmb: Whose fault is it?
    reasmb: Does assigning fault help?

key: responsible 4
  decomp: * i am responsible *
    reasmb: What are you responsible for?
    reasmb: Is this responsibility a burden?
    reasmb: How does this responsibility affect you?
  decomp: *
    reasmb: Who is responsible?
    reasmb: What does responsibility mean to you?

key: deserve 4
  decomp: * i deserve *
    reasmb: Why do you think you deserve (2)?
    reasmb: What makes you deserve (2)?
  decomp: * i don't deserve *
    reasmb: Why don't you think you deserve (2)?
    reasmb: Who told you that you don't deserve (2)?
    reasmb: What would it mean to deserve (2)?
  decomp: *
    reasmb: What do you think you deserve?
    reasmb: Is this about deserving?

key: fair 3
  decomp: * not fair *
    reasmb: What isn't fair?
    reasmb: Why is it unfair?
    reasmb: How do you cope with unfairness?
  decomp: *
    reasmb: Is fairness important to you?
    reasmb: What does fair mean to you?

key: justice 3
  decomp: *
    reasmb: What does justice mean to you?
    reasmb: Are you seeking justice?
    reasmb: Is this about right and wrong?

key: selfish 4
  decomp: * i am selfish *
    reasmb: What makes you think you're selfish?
    reasmb: Is taking care of yourself selfish?
    reasmb: Who told you you were selfish?
  decomp: *
    reasmb: Is selfishness a concern?
    reasmb: What does selfish mean to you?

key: perfect 4
  decomp: * i am not perfect *
    reasmb: Who is perfect?
    reasmb: Why do you need to be perfect?
    reasmb: What would perfection look like?
  decomp: * perfect *
    reasmb: Is perfection important to you?
    reasmb: Are you a perfectionist?
    reasmb: What does perfection mean to you?

key: enough 3
  decomp: * not enough *
    reasmb: What isn't enough?
    reasmb: What would be enough?
    reasmb: Who decides what's enough?
  decomp: * i am not enough *
    reasmb: What makes you feel you're not enough?
    reasmb: Not enough for whom?
    reasmb: What would being enough look like?
  decomp: *
    reasmb: Is this about having enough?
    reasmb: What would enough be?

key: better 3
  decomp: * i want to be better *
    reasmb: Better in what way?
    reasmb: What would being better look like?
    reasmb: Are you too hard on yourself?
  decomp: * get better *
    reasmb: What would getting better mean?
    reasmb: How would you know if you got better?
  decomp: *
    reasmb: Better than what?
    reasmb: What does better mean to you?

key: worse 3
  decomp: * getting worse *
    reasmb: What's getting worse?
    reasmb: How long has it been getting worse?
    reasmb: What would make it better?
  decomp: *
    reasmb: In what way is it worse?
    reasmb: What would prevent it from getting worse?

key: normal 3
  decomp: * i am not normal *
    reasmb: What is normal?
    reasmb: Who decides what's normal?
    reasmb: Would being normal make you happier?
  decomp: * normal *
    reasmb: What does normal mean to you?
    reasmb: Is being normal important?

key: crazy 4
  decomp: * i am crazy *
    reasmb: What makes you think you're crazy?
    reasmb: Who told you you're crazy?
    reasmb: What does crazy mean to you?
  decomp: * crazy *
    reasmb: In what way is it crazy?
    reasmb: What do you mean by crazy?

key: stupid 4
  decomp: * i am stupid *
    reasmb: Why do you call yourself stupid?
    reasmb: Who told you you're stupid?
    reasmb: Is that what you really believe?
  decomp: *
    reasmb: Why do you say that?
    reasmb: What makes something stupid?

key: smart 2
  decomp: * i am not smart *
    reasmb: What makes you think you're not smart?
    reasmb: Intelligence comes in many forms.
    reasmb: Who told you you're not smart?
  decomp: *
    reasmb: Is intelligence important to you?

key: ugly 4
  decomp: * i am ugly *
    reasmb: Why do you think you're ugly?
    reasmb: Who told you you're ugly?
    reasmb: Is appearance very important to you?
  decomp: *
    reasmb: What makes something ugly to you?

key: beautiful 2
  decomp: *
    reasmb: What do you find beautiful?
    reasmb: Is beauty important to you?

key: body 4
  decomp: * my body *
    reasmb: How do you feel about your body?
    reasmb: What about your body concerns you?
    reasmb: Is your body causing you distress?
  decomp: *
    reasmb: What role does your body play in this?

key: weight 4
  decomp: * my weight *
    reasmb: How do you feel about your weight?
    reasmb: Is weight a concern for you?
    reasmb: What about your weight bothers you?
  decomp: *
    reasmb: Is weight an issue for you?

key: food 3
  decomp: *
    reasmb: What's your relationship with food?
    reasmb: Is eating an issue for you?
    reasmb: How do you feel about food?

key: eat 3
  decomp: * i don't eat *
    reasmb: Why don't you eat?
    reasmb: How long has this been happening?
    reasmb: Is eating difficult for you?
  decomp: * i eat too much *
    reasmb: What triggers overeating for you?
    reasmb: How does eating too much affect you?
  decomp: *
    reasmb: How is your eating?
    reasmb: Is food a concern?

key: exercise 2
  decomp: *
    reasmb: How is your exercise routine?
    reasmb: Is physical activity important to you?

key: people 3
  decomp: * people *
    reasmb: What people specifically?
    reasmb: How do people affect you?
    reasmb: What about people concerns you?
  decomp: *
    reasmb: Are people a source of stress?
    reasmb: How do you feel about people in general?

key: society 3
  decomp: *
    reasmb: How do you feel about society?
    reasmb: Does society pressure you?
    reasmb: What about society concerns you?

key: world 3
  decomp: * the world *
    reasmb: How do you see the world?
    reasmb: What about the world concerns you?
    reasmb: Is the world a difficult place for you?
  decomp: *
    reasmb: What role does the world play in this?

key: home 3
  decomp: * my home *
    reasmb: Tell me about your home.
    reasmb: Is home a safe place for you?
    reasmb: What's happening at home?
  decomp: *
    reasmb: Is home important to you?
    reasmb: How do you feel at home?

key: safe 4
  decomp: * i don't feel safe *
    reasmb: What's making you feel unsafe?
    reasmb: Where do you feel safe?
    reasmb: How long have you felt unsafe?
  decomp: *
    reasmb: Is safety a concern for you?
    reasmb: What would help you feel safe?

key: danger 5
  decomp: *
    reasmb: What danger are you facing?
    reasmb: Are you in danger?
    reasmb: Tell me about this danger.

key: abuse 6
  decomp: *
    reasmb: Are you being abused?
    reasmb: Tell me about the abuse.
    reasmb: Have you told anyone else about this abuse?
    reasmb: Your safety is important.

key: violence 6
  decomp: *
    reasmb: Are you experiencing violence?
    reasmb: Tell me about this violence.
    reasmb: Is there somewhere safe you can go?

key: trauma 5
  decomp: *
    reasmb: Tell me about your trauma.
    reasmb: How long have you been dealing with this trauma?
    reasmb: Have you sought help for trauma?
    reasmb: Trauma can have lasting effects.

key: nightmares 4
  decomp: *
    reasmb: Tell me about your nightmares.
    reasmb: How often do you have nightmares?
    reasmb: What are the nightmares about?

key: flashback 5
  decomp: *
    reasmb: Tell me about these flashbacks.
    reasmb: What triggers your flashbacks?
    reasmb: How do you cope with flashbacks?

key: panic 5
  decomp: * panic attack *
    reasmb: Tell me about your panic attacks.
    reasmb: How often do you have panic attacks?
    reasmb: What triggers your panic attacks?
  decomp: *
    reasmb: Are you experiencing panic?
    reasmb: What's causing this panic?

key: breathe 4
  decomp: * can't breathe *
    reasmb: Are you having trouble breathing right now?
    reasmb: What's making it hard to breathe?
    reasmb: Try to take slow, deep breaths.
  decomp: *
    reasmb: How is your breathing?
    reasmb: Is breathing difficult sometimes?

key: cry 3
  decomp: * i cry *
    reasmb: What makes you cry?
    reasmb: How often do you cry?
    reasmb: Is crying a release for you?
  decomp: * i can't cry *
    reasmb: Why can't you cry?
    reasmb: Would you like to be able to cry?
  decomp: *
    reasmb: Crying can be healing.
    reasmb: How do you feel about crying?

key: scream 3
  decomp: * i want to scream *
    reasmb: What makes you want to scream?
    reasmb: What's building up inside you?
    reasmb: Have you tried expressing this feeling?
  decomp: *
    reasmb: What's making you want to scream?

key: angry 4
  decomp: * i am angry *
    reasmb: What makes you angry?
    reasmb: How do you express your anger?
    reasmb: What happens when you get angry?
  decomp: * angry at *
    reasmb: Why are you angry at (2)?
    reasmb: What did (2) do?
    reasmb: How long have you been angry at (2)?
  decomp: *
    reasmb: Tell me about your anger.
    reasmb: How do you handle anger?

key: mad 3
  decomp: * i am mad *
    reasmb: What are you mad about?
    reasmb: How do you handle being mad?
  decomp: *
    reasmb: goto angry

key: furious 4
  decomp: *
    reasmb: What's making you so furious?
    reasmb: That sounds very intense.
    reasmb: goto angry

key: rage 5
  decomp: *
    reasmb: Tell me about this rage.
    reasmb: What triggers your rage?
    reasmb: How do you handle such intense anger?

key: bitter 4
  decomp: * i am bitter *
    reasmb: What's making you bitter?
    reasmb: How long have you felt bitter?
    reasmb: What would help release this bitterness?
  decomp: *
    reasmb: Tell me about this bitterness.
    reasmb: What's causing the bitterness?

key: resentment 4
  decomp: *
    reasmb: What are you resentful about?
    reasmb: Who do you resent?
    reasmb: How is resentment affecting you?

key: resent 4
  decomp: * i resent *
    reasmb: Why do you resent (2)?
    reasmb: How long have you resented (2)?
    reasmb: How is this resentment affecting you?
  decomp: *
    reasmb: goto resentment

key: suffer 5
  decomp: * i suffer *
    reasmb: What causes your suffering?
    reasmb: How long have you been suffering?
    reasmb: What would end your suffering?
  decomp: *
    reasmb: Tell me about your suffering.
    reasmb: What kind of suffering are you experiencing?

key: struggle 4
  decomp: * i struggle *
    reasmb: What do you struggle with?
    reasmb: How long have you been struggling?
    reasmb: What would ease this struggle?
  decomp: *
    reasmb: What are you struggling with?
    reasmb: Tell me about your struggles.

key: survive 4
  decomp: * i survive *
    reasmb: What are you surviving?
    reasmb: Survival takes strength.
  decomp: *
    reasmb: Is survival a concern?
    reasmb: What are you trying to survive?

key: cope 3
  decomp: * i can't cope *
    reasmb: What can't you cope with?
    reasmb: What would help you cope?
    reasmb: How have you coped in the past?
  decomp: *
    reasmb: How are you coping?
    reasmb: What helps you cope?

key: deal 3
  decomp: * i can't deal *
    reasmb: What can't you deal with?
    reasmb: What would help you deal with this?
  decomp: *
    reasmb: How are you dealing with things?
    reasmb: Is dealing with this difficult?

key: handle 3
  decomp: * i can't handle *
    reasmb: What can't you handle?
    reasmb: What would make it more manageable?
  decomp: *
    reasmb: How are you handling things?
    reasmb: Is this hard to handle?

key: manage 3
  decomp: * i can't manage *
    reasmb: What can't you manage?
    reasmb: What would help you manage?
  decomp: *
    reasmb: How are you managing?
    reasmb: Is management a challenge?

key: strong 3
  decomp: * i am not strong *
    reasmb: What makes you think you're not strong?
    reasmb: Strength comes in many forms.
    reasmb: Being here takes strength.
  decomp: * i have to be strong *
    reasmb: Why do you have to be strong?
    reasmb: What would happen if you weren't strong?
    reasmb: Who told you that you have to be strong?
  decomp: *
    reasmb: What does being strong mean to you?

key: weak 4
  decomp: * i am weak *
    reasmb: What makes you feel weak?
    reasmb: Is weakness bad?
    reasmb: Who told you you're weak?
  decomp: *
    reasmb: Is weakness a concern?
    reasmb: What does weak mean to you?

key: vulnerable 4
  decomp: * i feel vulnerable *
    reasmb: What makes you feel vulnerable?
    reasmb: Is vulnerability difficult for you?
    reasmb: What would help you feel less vulnerable?
  decomp: *
    reasmb: Vulnerability can be difficult.
    reasmb: How do you handle vulnerability?

key: sensitive 3
  decomp: * i am too sensitive *
    reasmb: Who told you you're too sensitive?
    reasmb: Is being sensitive a problem?
    reasmb: Sensitivity can be a gift.
  decomp: *
    reasmb: Is sensitivity an issue for you?

key: emotional 3
  decomp: * i am too emotional *
    reasmb: Who told you you're too emotional?
    reasmb: What's wrong with having emotions?
    reasmb: How do you handle your emotions?
  decomp: *
    reasmb: How do you feel about your emotions?
    reasmb: Are emotions difficult for you?

key: feelings 3
  decomp: * my feelings *
    reasmb: Tell me about your feelings.
    reasmb: How do you handle your feelings?
    reasmb: What are you feeling right now?
  decomp: *
    reasmb: How are you feeling?
    reasmb: What feelings are coming up?

key: heart 4
  decomp: * my heart *
    reasmb: What's in your heart?
    reasmb: What does your heart tell you?
    reasmb: Is your heart heavy?
  decomp: * broken heart *
    reasmb: Tell me about your broken heart.
    reasmb: What broke your heart?
    reasmb: Heartbreak is painful.
  decomp: *
    reasmb: Is this a matter of the heart?

key: mind 3
  decomp: * my mind *
    reasmb: What's on your mind?
    reasmb: How is your mind treating you?
    reasmb: Is your mind racing?
  decomp: * lose my mind *
    reasmb: What makes you feel you're losing your mind?
    reasmb: That sounds very distressing.
  decomp: *
    reasmb: Is something on your mind?

key: soul 4
  decomp: * my soul *
    reasmb: What's happening to your soul?
    reasmb: What does your soul need?
  decomp: *
    reasmb: Is this a matter of the soul?

key: spirit 3
  decomp: * my spirit *
    reasmb: How is your spirit?
    reasmb: Is your spirit troubled?
  decomp: *
    reasmb: goto soul

key: energy 3
  decomp: * no energy *
    reasmb: What's draining your energy?
    reasmb: How long have you had no energy?
    reasmb: What would give you energy?
  decomp: *
    reasmb: How is your energy level?
    reasmb: Is energy a problem?

key: motivation 3
  decomp: * no motivation *
    reasmb: What's affecting your motivation?
    reasmb: What would motivate you?
    reasmb: How long have you lacked motivation?
  decomp: *
    reasmb: Is motivation a challenge?
    reasmb: What motivates you?

key: focus 3
  decomp: * i can't focus *
    reasmb: What's distracting you?
    reasmb: How long have you had trouble focusing?
    reasmb: What would help you focus?
  decomp: *
    reasmb: Is focus a problem?
    reasmb: What helps you focus?

key: concentrate 3
  decomp: * i can't concentrate *
    reasmb: What's preventing concentration?
    reasmb: How long has this been happening?
  decomp: *
    reasmb: goto focus

key: distracted 3
  decomp: *
    reasmb: What's distracting you?
    reasmb: How do distractions affect you?
    reasmb: goto focus

key: racing 4
  decomp: * racing thoughts *
    reasmb: What are your thoughts racing about?
    reasmb: How do you slow them down?
    reasmb: How long have you had racing thoughts?
  decomp: * mind racing *
    reasmb: What's making your mind race?
    reasmb: This sounds exhausting.
  decomp: *
    reasmb: What's racing?

key: obsess 4
  decomp: * i obsess *
    reasmb: What do you obsess about?
    reasmb: How long have you been obsessing?
    reasmb: How does obsessing affect you?
  decomp: *
    reasmb: Are you obsessing over something?
    reasmb: Tell me about these obsessive thoughts.

key: ruminate 4
  decomp: *
    reasmb: What are you ruminating about?
    reasmb: How do you stop ruminating?
    reasmb: goto obsess

key: overthink 4
  decomp: * i overthink *
    reasmb: What do you overthink?
    reasmb: How does overthinking affect you?
    reasmb: What would help you think less?
  decomp: *
    reasmb: Are you an overthinker?
    reasmb: What are you overthinking?

key: worry 4
  decomp: * i worry *
    reasmb: What do you worry about?
    reasmb: How much time do you spend worrying?
    reasmb: Does worrying help you?
  decomp: *
    reasmb: What are you worried about?
    reasmb: goto worried

key: doubt 3
  decomp: * i doubt *
    reasmb: What do you doubt?
    reasmb: Why do you doubt (2)?
    reasmb: How does doubt affect you?
  decomp: *
    reasmb: What are you doubting?
    reasmb: Is doubt common for you?

key: confident 3
  decomp: * i am not confident *
    reasmb: What undermines your confidence?
    reasmb: Have you ever felt confident?
    reasmb: What would build your confidence?
  decomp: *
    reasmb: How is your confidence?
    reasmb: Is confidence an issue?

key: insecure 4
  decomp: * i am insecure *
    reasmb: What makes you feel insecure?
    reasmb: Where does this insecurity come from?
    reasmb: How long have you felt insecure?
  decomp: *
    reasmb: Tell me about your insecurity.
    reasmb: What triggers your insecurity?

key: self 4
  decomp: * myself *
    reasmb: Tell me more about yourself.
    reasmb: How do you see yourself?
    reasmb: What's your relationship with yourself?
  decomp: * self *
    reasmb: How do you feel about yourself?
    reasmb: Is your sense of self strong?

key: identity 4
  decomp: * my identity *
    reasmb: Tell me about your identity.
    reasmb: How do you define yourself?
    reasmb: Is your identity clear to you?
  decomp: *
    reasmb: Who are you?
    reasmb: How do you see yourself?

key: real 3
  decomp: * not real *
    reasmb: What doesn't feel real?
    reasmb: How long has this felt unreal?
  decomp: * feel real *
    reasmb: What would make things feel real?
  decomp: *
    reasmb: What is real to you?

key: exist 4
  decomp: * i don't exist *
    reasmb: What makes you feel you don't exist?
    reasmb: That sounds very distressing.
  decomp: *
    reasmb: What does existence mean to you?

key: belong 4
  decomp: * i don't belong *
    reasmb: Where do you feel you don't belong?
    reasmb: What would help you feel you belong?
    reasmb: Have you ever felt you belonged?
  decomp: *
    reasmb: Is belonging important to you?
    reasmb: Where do you feel you belong?

key: fit 3
  decomp: * i don't fit *
    reasmb: Where don't you fit?
    reasmb: Have you ever felt you fit in?
  decomp: *
    reasmb: goto belong

key: connect 4
  decomp: * i can't connect *
    reasmb: What's preventing connection?
    reasmb: Who do you want to connect with?
    reasmb: How long have you felt disconnected?
  decomp: *
    reasmb: Is connection important to you?
    reasmb: How do you connect with others?

key: disconnect 4
  decomp: * i feel disconnected *
    reasmb: From what or whom do you feel disconnected?
    reasmb: How long have you felt this way?
    reasmb: What would help you reconnect?
  decomp: *
    reasmb: goto connect

key: isolate 4
  decomp: * i isolate *
    reasmb: Why do you isolate yourself?
    reasmb: Does isolation help or hurt you?
    reasmb: How long have you been isolating?
  decomp: *
    reasmb: Are you isolating yourself?
    reasmb: goto alone

key: withdraw 4
  decomp: * i withdraw *
    reasmb: What makes you withdraw?
    reasmb: Who do you withdraw from?
    reasmb: Does withdrawing help?
  decomp: *
    reasmb: goto isolate

key: communicate 3
  decomp: * i can't communicate *
    reasmb: What's blocking communication?
    reasmb: Who do you want to communicate with?
  decomp: *
    reasmb: How is your communication?
    reasmb: Is communication difficult?

key: talk 3
  decomp: * i can't talk *
    reasmb: What can't you talk about?
    reasmb: Who can't you talk to?
  decomp: * no one to talk *
    reasmb: That sounds lonely.
    reasmb: I'm here to talk to.
  decomp: *
    reasmb: Who do you talk to?
    reasmb: Is talking helpful for you?

key: listen 3
  decomp: * no one listens *
    reasmb: That must feel frustrating.
    reasmb: I'm listening to you.
    reasmb: What do you want people to hear?
  decomp: *
    reasmb: Do you feel heard?
    reasmb: Is listening important to you?

key: hear 3
  decomp: * no one hears *
    reasmb: goto listen
  decomp: *
    reasmb: What do you want to be heard?

key: seen 3
  decomp: * no one sees *
    reasmb: Do you feel invisible?
    reasmb: What would being seen mean to you?
  decomp: * i want to be seen *
    reasmb: What does being seen mean to you?
    reasmb: Who do you want to see you?
  decomp: *
    reasmb: Is being seen important?

key: invisible 4
  decomp: * i feel invisible *
    reasmb: What makes you feel invisible?
    reasmb: Who doesn't see you?
    reasmb: How long have you felt invisible?
  decomp: *
    reasmb: Do you sometimes feel invisible?
    reasmb: What would visibility look like?

key: ignore 4
  decomp: * ignore me *
    reasmb: Who ignores you?
    reasmb: How does being ignored make you feel?
    reasmb: What would you like them to notice?
  decomp: * i ignore *
    reasmb: What do you ignore?
    reasmb: Why do you ignore (2)?
  decomp: *
    reasmb: Is ignoring a problem?

key: reject 5
  decomp: * reject me *
    reasmb: Who rejects you?
    reasmb: How does rejection feel?
    reasmb: Have you always feared rejection?
  decomp: * rejected *
    reasmb: Tell me about feeling rejected.
    reasmb: What happened?
  decomp: *
    reasmb: Is rejection a fear of yours?

key: abandon 5
  decomp: * abandon me *
    reasmb: Who has abandoned you?
    reasmb: Do you fear abandonment?
    reasmb: How does abandonment affect you?
  decomp: * abandoned *
    reasmb: Tell me about feeling abandoned.
    reasmb: Who abandoned you?
  decomp: *
    reasmb: Is abandonment a concern?

key: betray 5
  decomp: * betray me *
    reasmb: Who betrayed you?
    reasmb: What did they do?
    reasmb: How has the betrayal affected you?
  decomp: * betrayed *
    reasmb: Tell me about the betrayal.
    reasmb: How are you coping with being betrayed?
  decomp: *
    reasmb: Has someone betrayed you?

key: trust 4
  decomp: * i can't trust *
    reasmb: Why can't you trust?
    reasmb: Who has broken your trust?
    reasmb: What would help you trust again?
  decomp: * i don't trust *
    reasmb: What makes trust difficult?
    reasmb: Have you been hurt by trusting?
  decomp: * trust *
    reasmb: Is trust difficult for you?
    reasmb: Tell me about trust.

key: honest 3
  decomp: *
    reasmb: Is honesty important to you?
    reasmb: Are you being honest with yourself?

key: pretend 3
  decomp: * i pretend *
    reasmb: What do you pretend?
    reasmb: Why do you pretend?
    reasmb: Who are you pretending for?
  decomp: *
    reasmb: Is pretending common for you?
    reasmb: What are you pretending?

key: fake 4
  decomp: * i feel fake *
    reasmb: In what way do you feel fake?
    reasmb: Who is the real you?
    reasmb: What would being authentic look like?
  decomp: *
    reasmb: What feels fake?
    reasmb: goto pretend

key: mask 4
  decomp: * wear a mask *
    reasmb: What mask do you wear?
    reasmb: Why do you wear this mask?
    reasmb: What's behind the mask?
  decomp: *
    reasmb: Are you hiding behind a mask?

key: authentic 3
  decomp: *
    reasmb: What does authentic mean to you?
    reasmb: Are you being your authentic self?

key: true 3
  decomp: * true self *
    reasmb: What is your true self like?
    reasmb: Do you show your true self?
  decomp: *
    reasmb: What is true for you?

key: honest 3
  decomp: * i am not honest *
    reasmb: Who are you not honest with?
    reasmb: What are you dishonest about?
  decomp: *
    reasmb: Is honesty difficult?
    reasmb: What does honesty mean to you?

key: defensive 3
  decomp: *
    reasmb: What are you defending against?
    reasmb: Is defensiveness a pattern for you?

key: protect 4
  decomp: * i protect *
    reasmb: What are you protecting?
    reasmb: Why do you feel the need to protect?
  decomp: * protect myself *
    reasmb: What are you protecting yourself from?
    reasmb: Is this protection necessary?
  decomp: *
    reasmb: What needs protection?

key: boundaries 4
  decomp: * my boundaries *
    reasmb: Tell me about your boundaries.
    reasmb: Are your boundaries respected?
    reasmb: Do you have trouble setting boundaries?
  decomp: *
    reasmb: Are boundaries an issue for you?
    reasmb: How are your boundaries?

key: say 2
  decomp: * i can't say *
    reasmb: What can't you say?
    reasmb: Who can't you say this to?
  decomp: * say no *
    reasmb: Is it hard to say no?
    reasmb: What happens when you try to say no?
  decomp: *
    reasmb: What do you want to say?

key: express 3
  decomp: * i can't express *
    reasmb: What can't you express?
    reasmb: What blocks your expression?
  decomp: *
    reasmb: Is expression difficult for you?
    reasmb: How do you express yourself?

key: share 3
  decomp: * i can't share *
    reasmb: What can't you share?
    reasmb: What makes sharing difficult?
  decomp: *
    reasmb: Is sharing difficult for you?

key: open 3
  decomp: * i can't open up *
    reasmb: What prevents you from opening up?
    reasmb: Who do you want to open up to?
  decomp: *
    reasmb: Is being open difficult?
    reasmb: How do you feel about being open?

key: close 3
  decomp: * i close off *
    reasmb: Why do you close off?
    reasmb: What triggers you to close off?
  decomp: *
    reasmb: Do you tend to close yourself off?

key: shut 3
  decomp: * i shut down *
    reasmb: What causes you to shut down?
    reasmb: What happens when you shut down?
  decomp: *
    reasmb: goto close
"""

from .eliza import Eliza
