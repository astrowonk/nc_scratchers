# Frequently Asked Questions

## What is this site doing exactly? 

The winners of a scratch off lottery ticket are determined at printing and randomly distributed throughout the tickets sold in stores. As tickets get sold, for some games, the winning tickets sell faster or slower than others. For example, imagine a jar was filled with 100 jelly beans and 2 were red, and the rest were green. If you took out 20 jelly beans and they were all green, the next person would have a better chance of getting the red bean.

For every state scratch off game, the North Carolina Lottery lists on their web site how many winning tickets are unclaimed for each prize. That information can be used to figure out which games have better or worse odds than their initial odds at printing. The Virginia version I made originally is still [here](https://marcoshuerta.com/scratch_to_win/).

## How does it work?

I estimate for each game how many tickets remain unsold. For each prize, I compare how many winning tickets are left and compare to the number of tickets left. Some prizes will have their overall odds improve, if tickets are being purchased at a faster rate than prizes are being claimed. For example if 80% of tickets have been sold but 2 of the 4 top prizes are still unclaimed, than the odds have improved from what is printed on the tickets.

## So I should definitely play the games you recommend?

Playing the lottery is generally a bad idea. But, if you're going to buy an NC scratcher, maybe? A lot of assumptions have to be made about the calculations. For example, I don't actually know how many tickets have been sold - the NC Lottery may not even know that per game, they don't share that information. I have to use the claim rate of the common small-prize tickets to *estimate* how many tickets are left unsold. That's just one assumption that is required.

## Wait, what else are you assuming? And what could be wrong with these assumptions?

Well, for example the most common prize can be just winning back your original $1 wager. Not everyone bothers to claim a $1 "winning" ticket. The North Carolina Lottery has said that 1.5% of total prize values goes unclaimed. Presumably most of that is the smallest prizes.

In any event, using the smallest prize claim rate to estimate how many tickets are left seems wrong: when I do that it shows that every game is getting worse odds which doesn't make sense. I use the most expensive ticket (so people likely will claim them) that still has relatively large number of winners at printing.

Another, bigger, problem in that people who win a small prize can claim it easily at any lottery retailer. So, those prize claims will fill in over a weekend. But if you win like $5000 you will have to go a lottery office, so those will never be claimed on a weekend.

For a big prize, like $500,000, those have taken ~2 weeks to claim after purchase. So, a game may *look* like it has improved odds, but in reality a winning ticket could have been sold a week ago and the winner is just waiting to claim it.

## So, it doesn't matter what ticket I buy? 

Well, it is probably a bad idea to buy tickets where we know the top prizes are all gone or have been claimed at a higher rate than sales. The game recommendations here should be better than buying a ticket from a clearly actively bad game or picking one randomly.

## What is expectation value? And why do are they all below $1, especially the cheap games? 

Expectation value is the statistical value of $1 played on that particular ticket. Imagine there were one hundred $1 tickets and half paid out $2, half nothing. The expectation value would be $1, because if you played forever (or if you bought every ticket), you'd break even (spend $100 on tickets, win $100 back on the 50 winners). Expectation value depends on the odds, but also the payout and the ticket price. Scratch off games have a house edge so that the prizes are less than the total revenue for selling the tickets (that's how the lottery makes money.)

The North Carolina lottery states that 75% of revenue goes to prizes, but that is not consistent for every game. Some scratch-off games have an expectation value starting around 60 cents per dollar (as of Fall 2026, every game with a $1 ticket cost had expectation values that started around 60 cents), others start closer to 80 cents (usually the most expensive scratch-offs).

However a lot of the expectation value comes from the top prize, with the longest odds, and a lot of the *improvement* in the expectation value comes from the top prizes going unclaimed. So while mathematically the odds are better, in reality it's still a long shot.

## So if the expectation value gets over $1, I should definitely play?

Sort of? It depends on the cost of the ticket, and your tolerance for risk/loss. If the expectation value is like $1.01, would you spend $1000 for the statistical edge of winning maybe (probably) $10?

And usually, as I said above, the expectation value is driven by an elevated chance of winning the top prize; which may just be unclaimed not still for sale and is still very long odds to win.

Also, the highest expectation values tend to be the highest cost tickets, so those are all games one can't play for very long before hitting one's spending limit. And then there is the ever-present risk that the expectation value is being driven by an assumption about a top prize remaining unsold when it is just unclaimed and the winner is waiting a a week or more to claim it.

