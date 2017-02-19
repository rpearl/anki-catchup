#CatchUp

Catchup is an Anki plugin used when behind by multiple days of reviews, because coming back after (illness, vacation, depressive episode, other) to the wall of 1000+ reviews is awful. It does this by suspending past-due cards, then unsuspending n day's worth of cards at a time.

This is somewhat antithetical to the Idea of Anki, because you're supposed to do reviews daily, but even more antithetical to the Idea of Anki is not doing reviews for a month because the backlog is too big and imposing, or getting burnt out while catching up, or deleting a deck and starting over because the backlog is too imposing. Human nature can be unhelpful; CatchUp is intended to help get around this.

Why not use filtered decks?: because I'm hella lazy
look you could do all this manually, it wouldn't even be so hard! you wouldn't even need filtered decks! but i'm lazy. 

##How To Use

###Part 1: suspending past-due cards

* Tools > CatchUp
* set your additional filter: it uses the same syntax as the default anki browser
* optionally: change the tag; the default will be "catchup"
* save your config
* click "suspend" button 
* all cards that meet the filter & are past due will be suspended and tagged
* will display how many cards have been suspended

by default, stats "how many cards are tagged" and "how many days behind you are" are hidden, but can be displayed.

###Part 2: Unsuspending

* Tools > CatchUp
* fill in box for number n of how many days to unsuspend at a time
* optionally: can unsuspend based on a filter; only cards both tagged and meeting that filter will be unsuspended
* click "unsuspend" button
* all cards that were due on the oldest n days that have been tagged will be unsuspended


##Usage Examples

####the first:
you were stuck in your bed for a week, crushed by the Recent Events. you come back to anki on the 8th. you are behind by 7 days of reviews.

every day you run suspend, and then unsuspend 2 days. (on day 8, you unsuspend 1 and 2; on 9, 3 and 4; on 10, 5 and 6; on 11, 7 and 8; on 12, 9 and 10; on 13, 11 and 12; on 14, 13 and 14). 

####the second:
you go to japan for a week; you do no reviews in anki, instead spending your time actually using japanese at the go club. you come back on the 8th day, behind by 7 days of reviews.

you run suspend on the 8th day, and then unsuspend 2 days. (on 8, you do 1 and 2, on 9 you do 3 and 4). on 10 you feel great and crush 5, 6, 7; on 11 you feel super-motivated and do 8, 9, 10, 11.

####the third:

you had an art project that required you to live in a self-built hut in a lobster costume for week and not use any language. you come back to anki. you are behind by 7 days of reviews.

on the day you come back, you run suspension, but filter out (prop:due=0). afterwards, every day, you unsuspend one day: on day 8, you unsuspend 1 and answer 1 and 8; on day 9, you answer 2 and 9; on day 10, you answer 3 and 10...

####the fourth:

you have gone to a fairy party and return thinking only one night has gone by, but in reality, it's been 7 days.

you run suspension, filtering out (is:learn); on 8 you do all the learning cards, plus 1 and 2; on 9, 3 and 4... you are caught up after a week.

####the fifth:

you have mid-terms for all but one class (Biology), and then spring break. you totally bailed on doing any reviews because vacay. after a week, you come home. you have an exam on the 9th day. 

on the 8th, you run suspension, filtering out (deck:Biology); on 8, you do all your past-due biology cards. on the 9th, after your exam, you do 1 and 2; on the 10th, 3 and 4... you are caught up by the 15th.

####the sixth:

you have a hella intense project that you work on for a week, and you don't open anki for a week. you also have midterms on days 9 and 10, one in your European Art History class on rococo art, and one on Otaku Terminology in your Japanese Culture class.

on the 8th, you run suspension. on the 8th, you unsuspend only cards tagged with "rococo". on the 9th, after that exam, you unsuspend only cards tagged with "otaku". on the 10th, you start catching up on everything else.

---

all of these examples could've been done with tagging, filters, etc, but the plugin makes it a little more straightforward and less prone to human error.
