## Hello Everyone,

## This code is a Discord Bot App using python that I created to help to organize votes in Tiermaker tierlists.

So if you want to use, this is how to do it and how it works:

## How to do it:

# Set up the bot

1° You can download this code and save in a local folder.

2° In bot.run("KEY"), change the key to your bot Key (If you don't have one, you can check out how to create in [Discod Developers](https://discord.com/developers/docs/intro)

3° Now you need to go to [TierMaker](https://tiermaker.com) and choose the Tierlist that you want to, so save it as html and store in your bot folder, save the name as tierlist.html

4° Then invite the bot to your discord and start it.

# Set up the lists and run the bot

1° First you need to add the participants to "Participantes.txt", do it using the prefix TL! and command add, like this:
> TL!add

2° Now use the command tierlist to setup the file Options.txt
> TL!tierlist

3° Then you can start using command Start to do it and next for the others options.
> TL!Start

> TL!next

OBS: To use next, please make sure that you are waiting bot show the response within 30 seconds.
If you want change the time, you can change the line with asyncio:
> await asyncio.sleep(30)


# Please, let me know if you need any help using this or if you have any improvement.

Enjoy and regards,
