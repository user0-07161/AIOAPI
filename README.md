# AIOAPI
Yeah so...
I made this API because of [@realprydev](https://github.com/realprydev)'s discord bot Koopa, which used the vacefron API, till it shut down. As we needed a API, I created this, to cover most of the required functions by Koopa.

# NOTE: I didn't create the [Roboto font](https://fonts.google.com/selection?query=roboto), neither did I create the [crewmate images](https://www.reddit.com/r/AmongUs/comments/iut5y2/couldnt_find_many_pngs_of_the_among_us_characters/#lightbox). 

| URL example                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | Result                                                      |   |
|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------|---|
| `/api/ejected?name=user0_18272&impostor=false&crewmate=orange`                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | Returns an Image. Crewmate is orange, and not the impostor. |   |
| `/api/rankcard?username=user0_18272&avatar=https://cdn.discordapp.com/avatars/1213799919920484364/3b13f8d04b4cced3dbd9a7fdf35405f8.png?size=4096&level=10&rank=&currentxp=2244&nextlevelxp=2989&previouslevelxp=0&acustombg=https://media.discordapp.net/attachments/977470725730488360/1026557633731235894/Untitled165_20221003191308.jpg&xpcolor=F8F8F9&isboosting=false` | Returns an Image (rank card)                                                                                                                                                                                                                                                                                                                                                                                                                                                                   


But hold on, there are more commands work-in-progress!

How to run the API:
Quite simple: `python3 main.py`
After that open localhost:8000/yourcommand in a web browser
Have fun!
