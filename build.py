#!/usr/bin/env python3
"""Builds index.html for pittner/vision-board-for-weight-loss.

A single-purpose page for the high-intent "weight loss vision board" / "fitness vision board" /
"weight loss motivation" search intent (heavily searched in late December and January): 36 goals
in 6 groups (eating, movement, habits, mindset, sleep and recovery, tracking and milestones), each
with why it matters and a first step for this week, and a link that opens the free maker with that
goal and step already filled in (?goal=&step=&layout=text&mode=wallpaper, T-098), so it can go on
the phone lock screen. Plus 12 honest questions, a 45-minute plan, a box for your own goal, and FAQ.

No dependencies. Run: python3 build.py
"""
import html as _html
import json
import pathlib
from urllib.parse import urlencode

HERE = pathlib.Path(__file__).resolve().parent
URL = "https://pittner.github.io/vision-board-for-weight-loss/"
SRC = "ghpages_weightloss"
CAMPAIGN = "weightloss_2027"

# (group, [(goal, why it matters, a first step for this week)])
GROUPS = [
    ("Eating and nutrition", [
        ("Eat protein with every meal", "Protein keeps you full for hours, so you snack less without willpower.", "Pick one protein you like (eggs, yoghurt, chicken, beans) and add it to breakfast tomorrow"),
        ("Cook at home five days a week", "Home cooking has far fewer calories than takeout and costs less too.", "Write five simple dinners you already know and buy for three of them"),
        ("Fill half my plate with vegetables", "Vegetables let you eat a big plate for few calories.", "Buy two vegetables you actually like and add one to tonight's dinner"),
        ("Stop drinking my calories", "Soda, juice and fancy coffees hide a meal's worth of sugar.", "Swap one sugary drink a day for water or black coffee this week"),
        ("Use a smaller plate", "A smaller plate makes a normal portion look full and satisfying.", "Serve dinner on a side plate tonight and notice you still feel fed"),
        ("Plan treats instead of banning them", "A planned treat stops the all-or-nothing binge that ends most diets.", "Choose one treat you will enjoy this weekend, guilt-free"),
    ]),
    ("Movement and training", [
        ("Walk 8,000 steps a day", "Walking burns real calories and is the one habit people actually keep.", "Check your average steps and add one 15-minute walk a day"),
        ("Strength training twice a week", "Muscle burns calories at rest and keeps the weight off for good.", "Book two 30-minute slots and do squats, push-ups and rows at home"),
        ("Move for 20 minutes every morning", "Morning movement sets the tone and you cannot skip it later.", "Lay out your shoes tonight and do 20 minutes right after you wake"),
        ("Take the stairs and park further away", "Small movement adds up to hundreds of calories a week, free.", "Pick one daily moment to take the stairs starting tomorrow"),
        ("Try one workout I might enjoy", "Exercise you like is exercise you repeat; the best workout is the one you do.", "Pick one class, sport or video and try it once this week"),
        ("Stretch for five minutes at night", "Less stiffness means you keep moving instead of quitting sore.", "Do five minutes of easy stretching before bed tonight"),
    ]),
    ("Habits and consistency", [
        ("Track what I eat for 14 days", "You cannot change what you do not see; tracking beats guessing.", "Pick one free app or a notebook and log today's food"),
        ("Prep food on Sundays", "A prepped fridge makes the healthy choice the easy choice all week.", "Cook one big batch of a meal this Sunday and portion it"),
        ("Keep trigger foods out of the house", "You do not eat at midnight what is not in the cupboard.", "Give away or finish one snack you binge on and do not re-buy it"),
        ("Eat without a screen", "Distracted eating makes you eat more and notice it less.", "Eat one meal a day at the table with the phone in another room"),
        ("Drink a glass of water before meals", "Water fills the stomach and slows you down enough to feel full.", "Put a glass by the sink and drink it before lunch this week"),
        ("Weigh in once a week, same day", "A weekly weigh-in shows the trend without the daily noise.", "Choose your weigh-in day and set a repeating reminder"),
    ]),
    ("Mindset and motivation", [
        ("Measure progress in more than the scale", "Energy, sleep, clothes and strength change before the number does.", "Write down three non-scale wins you want to see by spring"),
        ("Be kind to myself after a slip", "One bad meal does not undo a week; guilt does more damage than the food.", "Decide now what you will say to yourself after the next slip"),
        ("Focus on the next 1 kg, not 20", "Small targets feel possible and keep you going past February.", "Set a first mini-goal you could reach in three to four weeks"),
        ("Find my real why", "A reason bigger than looks is what carries you on hard days.", "Write one sentence: I want this because..."),
        ("Celebrate the habit, not just the loss", "Rewarding consistency builds the behaviour that keeps weight off.", "Pick a non-food reward for two full weeks of your new habit"),
        ("Picture myself a year from now", "Seeing the future you makes today's choice easier.", "Describe in two lines how a healthy ordinary day looks in 2027"),
    ]),
    ("Sleep and stress", [
        ("Go to bed before 11 pm", "Short sleep raises hunger hormones and makes cravings win.", "Set a phone alarm for 10:30 pm called Start winding down"),
        ("Keep a regular sleep schedule", "Steady sleep steadies appetite and energy for training.", "Pick a wake time and keep it the same, even on weekends"),
        ("Walk when I'm stressed instead of snacking", "A short walk clears the urge that sends you to the cupboard.", "Next time you crave a snack from stress, walk for 10 minutes first"),
        ("Cut screens 30 minutes before bed", "Better wind-down means deeper sleep and fewer late-night snacks.", "Charge your phone outside the bedroom starting tonight"),
        ("Name my emotional-eating triggers", "You beat the pattern you can see coming.", "Write the two moments you most often eat without hunger"),
        ("Breathe for two minutes when I want to quit", "A short pause breaks the autopilot that ends plans.", "Try two minutes of slow breathing the next time motivation dips"),
    ]),
    ("Tracking and milestones", [
        ("Take monthly progress photos", "Photos show change your eyes miss day to day.", "Take a front and side photo today in the same spot and light"),
        ("Record my measurements", "A tape measure often moves when the scale is stuck.", "Measure your waist, hips and chest today and write them down"),
        ("Set a reward at every 5 kg", "Milestones turn a long road into a series of wins.", "Decide the first reward and what you have to reach to earn it"),
        ("Keep a streak I don't want to break", "A visible streak is a quiet, powerful reason to show up.", "Mark today on a calendar and aim not to break the chain"),
        ("Book a goal I'm training for", "An event on the calendar gives training a deadline and a purpose.", "Pick a 5k, a hike or a trip and put the date in your calendar"),
        ("Review and adjust every month", "What worked in month one often needs a tweak in month two.", "Set a monthly date to check your plan and change one thing"),
    ]),
]

QUESTIONS = [
    "Why do I want to lose weight, really, beyond how it looks?",
    "What has made past attempts stop, and when exactly did they stop?",
    "When do I eat without being hungry, and what is happening then?",
    "What healthy food do I actually enjoy, not just tolerate?",
    "What kind of movement have I ever kept up for more than a month?",
    "What does a realistic good day of eating look like for me?",
    "Who can support me, and who quietly makes it harder?",
    "What will I tell myself on the day the scale does not move?",
    "How much sleep am I really getting, and how does it change my cravings?",
    "What is one thing I can do for 10 minutes even on my worst day?",
    "What will I do differently the next time I slip?",
    "If this year goes really well, what is different about my body and energy by next winter?",
]

PLAN = [
    ("10 minutes: look back honestly.", "Write what stopped your past attempts and the moments you eat without hunger. The patterns point to your plan."),
    ("15 minutes: answer the questions.", "Go through the 12 questions below. Short, honest answers are enough; nobody else reads them."),
    ("10 minutes: pick three goals.", "Not ten. One for eating, one for movement, one for the habit or mindset that keeps tripping you up."),
    ("10 minutes: make it visible.", "Turn your most important goal and its first step into a phone lock screen, so you see it every time you reach for a snack."),
]

FAQ = [
    ("What should go on a weight loss vision board?",
     "Put the goal in your own words, a first step you can do this week, and a reminder of your real why. "
     "This page has 36 weight loss goals in 6 groups (eating, movement, habits, mindset, sleep, tracking), each with a first step, so you can pick three and make them visible."),
    ("Does a vision board actually help with weight loss?",
     "A board does not burn calories, but seeing your goal and your next step every day keeps the decision in front of you. "
     "The habit that works best is putting it on your phone lock screen, which you look at dozens of times a day, right when cravings hit."),
    ("How many goals should I put on it?",
     "Three is enough: one about what you eat, one about moving more, and one about the habit or feeling that keeps derailing you. Fewer goals get more attention and stick longer."),
    ("What are realistic weight loss goals for 2027?",
     "Small and specific beats big and vague: walk 8,000 steps a day, eat protein with every meal, cook at home five days a week, go to bed before 11 pm. "
     "Aim for the next 1 kg, not the final 20, and measure more than the scale."),
    ("Is the maker free?",
     "Yes. It runs in your browser, needs no account and uploads nothing. Save the image to your phone lock screen or print it."),
    ("Can I make a full weight loss vision board with all my goals?",
     "Yes. Start from your goals in the AI vision board generator: you see a free preview, and unlocking the full-size board is optional (8.99 EUR)."),
]

def e(s):
    return _html.escape(s, quote=True)


def link(path, **extra):
    q = dict(extra)
    q.update({"utm_source": SRC, "utm_medium": "referral", "utm_campaign": CAMPAIGN})
    return "https://visionboard.bemooore.com" + path + "?" + urlencode(q)


def maker(goal, step, content):
    return link("/free-vision-board-maker/", goal=goal, step=step, layout="text", mode="wallpaper", utm_content=content)


TOOL = link("/free-vision-board-maker/", mode="wallpaper", layout="text", utm_content="plan_tool")
AI = link("/en/create.php", utm_content="faq_ai")
AI_PLAN = link("/en/create.php", utm_content="plan_ai")
HOME = link("/", utm_content="footer_home")


def slug(s):
    return "-".join("".join(c if c.isalnum() else " " for c in s.lower()).split())


def build():
    count = sum(len(gs) for _, gs in GROUPS)
    nav = " ".join(f'<a class="chip" href="#{slug(g)}">{e(g)}</a>' for g, _ in GROUPS)
    blocks = []
    for g, goals in GROUPS:
        cards = []
        for i, (goal, why, step) in enumerate(goals, 1):
            cid = f"{slug(g)}_{i}"
            cards.append(
                f'      <div class="wcard" id="g-{cid}"><h3>{e(goal)}</h3><p>{e(why)}</p>'
                f'<p class="step"><span>First step this week:</span> {e(step)}</p>'
                f'<a class="btn" href="{e(maker(goal, step, "goal_" + cid))}" data-cta="goal_{cid}">Make it my lock screen</a></div>')
        blocks.append(f'  <section class="grp" id="{slug(g)}">\n    <h2>{e(g)}</h2>\n    <div class="grid">\n'
                      + "\n".join(cards) + "\n    </div>\n  </section>")
    questions = "\n".join(f"    <li>{e(q)}</li>" for q in QUESTIONS)
    plan = "\n".join(f"    <li><b>{e(a)}</b> {e(b)}</li>" for a, b in PLAN)
    faq_html = "\n".join(f"  <h3>{e(q)}</h3>\n  <p>{e(a)}</p>" for q, a in FAQ)
    ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
        ensure_ascii=False)
    page = TEMPLATE
    for k, v in {
        "%%NAV%%": nav, "%%GROUPS%%": "\n\n".join(blocks), "%%QUESTIONS%%": questions, "%%PLAN%%": plan,
        "%%FAQ%%": faq_html, "%%LD%%": ld, "%%COUNT%%": str(count), "%%NQ%%": str(len(QUESTIONS)),
        "%%TOOL%%": e(TOOL), "%%AI%%": e(AI), "%%AIPLAN%%": e(AI_PLAN), "%%HOME%%": e(HOME),
        "%%URL%%": URL, "%%SRC%%": SRC, "%%CAMPAIGN%%": CAMPAIGN,
    }.items():
        page = page.replace(k, v)
    (HERE / "index.html").write_text(page, encoding="utf-8")
    print("index.html", len(page.encode()), "bytes,", count, "goals")


TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Weight Loss Vision Board 2027: %%COUNT%% Goals with a First Step + Free Lock Screen</title>
<meta name="description" content="%%COUNT%% weight loss and fitness goals for 2027 (eating, movement, habits, mindset, sleep, tracking), each with a first step for this week, %%NQ%% honest questions and a 45-minute plan. Turn your goal into a free phone lock screen. No signup.">
<link rel="canonical" href="%%URL%%">
<meta property="og:type" content="website">
<meta property="og:title" content="Weight loss vision board 2027 - %%COUNT%% goals with a first step and a free lock screen">
<meta property="og:description" content="Weight loss and fitness goals with a first step, %%NQ%% questions, and a lock screen in one click. Free, no signup.">
<meta property="og:url" content="%%URL%%">
<style>
:root{--ink:#111827;--muted:#6B7280;--rule:#E5E7EB;--acc:#1D4ED8;--bg:#F8FAFD}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif}
a{color:var(--acc)}
.wrap{max-width:1000px;margin:0 auto;padding:0 20px}
header.hero{padding:48px 0 18px}
h1{font:600 clamp(28px,4.4vw,42px)/1.15 Georgia,"Times New Roman",serif;margin:0 0 14px;letter-spacing:-.01em}
.lede{font-size:18px;color:#374151;max-width:64ch;margin:0 0 14px}
.meta{font-size:14px;color:var(--muted);margin:0}
.btn{appearance:none;display:inline-block;text-decoration:none;border:1px solid #D1D5DB;background:#fff;color:var(--ink);padding:9px 15px;border-radius:999px;font:500 14px/1 inherit;cursor:pointer}
.btn:hover{border-color:var(--acc);color:var(--acc)}
.btn.primary{background:var(--acc);border-color:var(--acc);color:#fff}
.btn.primary:hover{background:#1E40AF;color:#fff}
.own{background:#fff;border:1px solid var(--rule);border-radius:16px;padding:18px;margin:8px 0 22px}
.own h2{font:600 21px/1.3 Georgia,serif;margin:0 0 10px}
.own .row{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1.3fr) auto;gap:8px;align-items:end}
@media (max-width:760px){.own .row{grid-template-columns:1fr}}
.own label{display:block;font-size:13px;color:var(--muted);margin:0 0 4px}
.own input{width:100%;border:1px solid #D1D5DB;border-radius:10px;padding:10px 12px;font:16px/1.3 inherit;background:#fff}
.own input:focus{outline:2px solid var(--acc);outline-offset:1px;border-color:var(--acc)}
#ownMsg{font-size:13px;color:var(--muted);margin:8px 0 0}
.chips{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 6px}
.chip{display:inline-block;text-decoration:none;border:1px solid var(--rule);background:#fff;color:#374151;padding:6px 12px;border-radius:999px;font-size:14px}
.chip:hover{border-color:var(--acc);color:var(--acc)}
section.grp{padding:22px 0 8px}
section.grp h2{font:600 24px/1.25 Georgia,serif;margin:0 0 12px}
.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
@media (max-width:860px){.grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:520px){.grid{grid-template-columns:1fr}}
.wcard{background:#fff;border:1px solid var(--rule);border-radius:14px;padding:14px 14px 16px;display:flex;flex-direction:column}
.wcard h3{font:600 19px/1.25 Georgia,serif;margin:0 0 6px}
.wcard p{margin:0 0 8px;color:#374151;font-size:15px}
.wcard .step{font-size:14px;color:var(--muted);flex:1}
.wcard .step span{color:var(--acc);font-weight:600}
.wcard .btn{align-self:flex-start}
section.block{padding:30px 0;border-top:1px solid var(--rule);margin-top:20px}
section.block h2{font:600 24px/1.25 Georgia,serif;margin:0 0 8px}
section.block>p{max-width:70ch;color:#374151}
ol.how,ol.qs{max-width:70ch;color:#374151;padding-left:22px}
ol.how li,ol.qs li{margin:0 0 10px}
.faq h3{font:600 16px/1.4 inherit;margin:18px 0 4px}
.faq p{margin:0;color:#374151;max-width:70ch}
footer{padding:28px 0 60px;font-size:14px;color:var(--muted);border-top:1px solid var(--rule)}
</style>
</head>
<body>
<div class="wrap">
<header class="hero">
  <h1>Weight loss vision board 2027: %%COUNT%% goals with a first step for this week</h1>
  <p class="lede">Most weight loss plans fail because the goal is vague and invisible by February. Below are %%COUNT%% weight loss and fitness goals, each with why it matters and a first step you can do this week, plus %%NQ%% honest questions to find out what really stopped you last time. Press a goal and it opens in a free maker with the first step under it: save it as your phone lock screen and see it every time a craving hits. No signup, nothing uploaded.</p>
  <p class="meta">%%COUNT%% goals in 6 groups &middot; %%NQ%% questions &middot; 45-minute plan &middot; lock screen in one click &middot; free, MIT licensed</p>
</header>

<div class="own" id="own">
  <h2>Already know your goal?</h2>
  <div class="row">
    <div><label for="ownGoal">My weight loss goal for 2027</label><input id="ownGoal" maxlength="120" placeholder="e.g. Walk 8,000 steps a day" autocomplete="off"></div>
    <div><label for="ownStep">First step (optional)</label><input id="ownStep" maxlength="120" placeholder="e.g. Add one 15-minute walk a day" autocomplete="off"></div>
    <button class="btn primary" id="ownGo" type="button">Make it my lock screen</button>
  </div>
  <p id="ownMsg">Opens the free maker with your goal filled in. Change colors or layout there, then save it to your phone or print it.</p>
</div>

<nav class="chips" aria-label="Groups">%%NAV%% <a class="chip" href="#questions">%%NQ%% questions</a> <a class="chip" href="#plan">45-minute plan</a></nav>

%%GROUPS%%

<section class="block" id="questions">
  <h2>%%NQ%% honest questions before you choose your goals</h2>
  <p>Answer them alone, with a notebook, in 15 minutes. Be honest, nobody else reads it. The answers that surprise you point to the goals that will actually stick.</p>
  <ol class="qs">
%%QUESTIONS%%
  </ol>
</section>

<section class="block" id="plan">
  <h2>Plan your weight loss year in 45 minutes</h2>
  <ol class="how">
%%PLAN%%
  </ol>
  <p><a class="btn primary" href="%%TOOL%%" data-cta="plan_tool">Open the free lock-screen maker</a>
     <a class="btn" href="%%AIPLAN%%" data-cta="plan_ai">Make a full board with all my goals</a></p>
</section>

<section class="block faq">
  <h2>Questions</h2>
%%FAQ%%
  <p style="margin-top:16px"><a class="btn" href="%%AI%%" data-cta="faq_ai">Make a full weight loss vision board</a></p>
</section>

<footer>
  MIT licensed &middot; published by the team behind
  <a href="%%HOME%%" data-cta="footer_home">visionboard.bemooore.com</a> &middot;
  more: <a href="https://pittner.github.io/new-year-resolutions-2027/">new year's resolutions 2027</a>,
  <a href="https://pittner.github.io/vision-board-for-career/">career vision board</a>,
  <a href="https://pittner.github.io/vision-board-for-family/">family vision board</a>,
  <a href="https://pittner.github.io/vision-board-for-couples/">vision board for couples</a>,
  <a href="https://pittner.github.io/vision-board-for-small-business/">small business vision board</a>,
  <a href="https://pittner.github.io/vision-board-for-students/">vision board for students</a>,
  <a href="https://pittner.github.io/word-of-the-year-2027/">word of the year 2027</a>,
  <a href="https://pittner.github.io/2027-vision-board-template/">printable 2027 vision board template</a>,
  <a href="https://pittner.github.io/vision-board-prompts/">54 vision board prompts</a>,
  <a href="https://pittner.github.io/">all free tools</a> &middot;
  <a href="https://github.com/pittner/vision-board-for-weight-loss">source</a>
</footer>
</div>

<script type="application/ld+json">
%%LD%%
</script>

<script>
(function(){
  var EP='https://visionboard.bemooore.com/api/event.php',P='%%SRC%%',engaged=false;
  function beacon(ev,label){
    try{
      var b=JSON.stringify({event:ev,utm:P+' | '+label+' | '+location.search});
      if(navigator.sendBeacon){navigator.sendBeacon(EP,new Blob([b],{type:'text/plain'}));}
      else{fetch(EP,{method:'POST',body:b,keepalive:true,mode:'no-cors'});}
    }catch(e){}
  }
  // Every link to our site carries where the visitor came from (e.g. chatgpt.com).
  var src=(location.search.match(/[?&]utm_source=([^&]+)/)||[])[1]||(document.referrer?document.referrer.split('/')[2]:'direct');
  Array.prototype.forEach.call(document.querySelectorAll('a[data-cta][href*="visionboard.bemooore.com"]'),function(a){
    a.href+='&utm_term='+encodeURIComponent('via_'+src);
  });
  function engage(how){ if(engaged)return; engaged=true; beacon('page_engaged',how); }
  setTimeout(function(){engage('dwell6s');},6000);
  window.addEventListener('scroll',function(){
    var h=document.documentElement;
    if((h.scrollTop||document.body.scrollTop)/((h.scrollHeight-h.clientHeight)||1)>0.25) engage('scroll25');
  },{passive:true});
  document.addEventListener('click',function(e){
    var a=e.target.closest('[data-cta]'); if(a) beacon('cta_click',a.getAttribute('data-cta'));
  });

  // Own goal: same prefill as the goal cards (?goal=&step=&layout=text&mode=wallpaper).
  var g=document.getElementById('ownGoal'),s=document.getElementById('ownStep'),msg=document.getElementById('ownMsg');
  function go(){
    var goal=g.value.trim(),step=s.value.trim();
    if(!goal){ msg.textContent='Type your goal first.'; g.focus(); return; }
    var q=new URLSearchParams({goal:goal,layout:'text',mode:'wallpaper',utm_source:P,utm_medium:'referral',
      utm_campaign:'%%CAMPAIGN%%',utm_content:'own_goal',utm_term:'via_'+src});
    if(step) q.set('step',step);
    beacon('cta_click','own_goal');
    location.href='https://visionboard.bemooore.com/free-vision-board-maker/?'+q.toString();
  }
  document.getElementById('ownGo').addEventListener('click',go);
  [g,s].forEach(function(el){ el.addEventListener('keydown',function(e){ if(e.key==='Enter') go(); }); });
})();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    build()
