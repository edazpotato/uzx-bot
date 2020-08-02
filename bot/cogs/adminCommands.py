import os
import ast
import json
import typing
import discord
import aiohttp
from discord.ext import commands
from bot.custom import embeds

def insert_returns(body):
    # insert return stmt if the last expression is a expression statement
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    # for if statements, we insert returns into the body and the orelse
    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    # for with blocks, again we insert returns into the body
    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)

class Admin(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot
        self.color = 0x03FCDB

    @commands.group(aliases=["a"])
    @commands.is_owner()
    async def admin(self, ctx):
        if ctx.invoked_subcommand is None:
            user = self.bot.get_user(int(self.bot.owner_id))
            data = {
                "title": "Hello *{0}*".format(user),
                "color": self.color
            }
            embed = embeds.RichEmbed(self.bot, data)
            await embed.send(ctx)

    @admin.command(name="raw", aliases=["r"])
    async def raw_subcommand(self, ctx, amount: typing.Optional[int] = 1):
        messages = await ctx.channel.history(limit=amount+1).flatten()
        message = messages[amount]
        msgcontent = discord.utils.escape_mentions(discord.utils.escape_markdown(message.content))
        data = {
            "color": self.color,
            "author": {
                "name": "{0}#{1}".format(message.author.name, message.author.discriminator),
                "icon_url": message.author.avatar_url
            },
            "description": "Raw message content:```\n\n{0}\n\n```".format(msgcontent)
        }
        embed = embeds.RichEmbed(self.bot, data)
        await embed.send(ctx)

    @admin.command(name="embed")
    async def embed_subcommand(self, ctx, *, data: typing.Optional[str]):
        json_acceptable_string = data.replace("'", "\"")
        d = json.loads(json_acceptable_string)
        if d is None:
            d = {
                "title": "ERROR: no embed code provided",
                "color": self.color
            }
        else:
            d = ast.literal_eval(data)
        embed = embeds.RichEmbed(self.bot, d)
        await embed.send(ctx)

    # spam genders 
    #@commands.is_owner() 
    #@commands.command(name="genderspam", hidden=True) 
    async def emoji_spam_command(self, ctx): 
        genders = ["Abimegender", "Absorgender", "Adamasgender", "Adeptogender", "Aerogender", "evaisgender", "Aesthetgender", "videgender", "Aethergender", "Affectugender", "Agender", "Agenderfluid", "cancegender", "Agenderflux", "librafluid", "Alexigender", "Aliusgender", "Ambigender", "Amaregender-", "Ambonec", "Amicagender", "Amogender", "flirtgender", "Amorgender", "Androgyne", "Anesigender", "Angeligender", "Angenital", "Anogender", "Anongender", "Antegender", "Antigender", "ungender", "Anxiegender", "Anvisgender", "apagender", "Apagender", "lethargender,", "inersgender", "anvisgender.", "Apconsugender", "Apogender", "Apollogender", "Aporagender", "Aptugender", "Aquarigender", "genderflow.", "Archaigender", "Arifluid", "arigender", "Arigender", "arifluid", "Arithmagender", "Argogender", "Astergender", "Astralgender", "Atmosgender", "Autigender-", "Autogender", "Axigender", "Batgender", "nocturnalgender", "Bigender", "Bigenderfluid", "Biogender", "Blizzgender", "wintegender", "Boggender", "swampgender", "Bordergender/Borderfluid", "Boyflux", "Brevigender", "Burstgender", "spikegender", "Cadensgender", "Cadogender", "Caedogender", "Caelgender", "Cancegender", "agenderfluid", "Canisgender", "Caprigender", "Carmigender", "Cassflux", "Cassgender", "Caveagender", "Cavusgender", "Cendgender", "Cennedgender", "Ceterofluid", "ceterogender", "Ceterogender", "Chaosgender", "Cheiragender", "Circgender", "Cloudgender", "Cocoongender", "Cogitofluid", "Cogitogender", "Coigender", "Collgender", "Colorgender", "Comgender", "Commogender-", "Condigender-", "Contigender", "Corugender", "Cosmicgender-", "Cryptogender", "Crystagender", "Cyclogender", "Daimogender", "Deaboy", "Delphigender", "Demifluid/flux", "Demigender", "Digigender", "Diurnalgender", "flowergender", "Domgender-", "Drakefluid", "Dryagender", "Dulcigender", "Duragender", "Eafluid", "enbyfluid", "Earthgender", "Egender", "exgender", "Ectogender", "Effreu", "effrille.", "effron", "Egogender", "(name)gender", "Ekragender", "Eldrigender", "Elegender", "Elementgender", "Elissogender", "Enbyfluid", "eafluid", "Endogender", "femfluid,", "mascfluid,", "nobifluid", "genderfluid,", "genderflux,", "horogender", "Energender", "Entheogender", "Entrogender", "Equigender", "Espigender", "Evaisgender", "aerogender,", "locugender.", "Exgender", "egender.", "Exiccogender", "Existigender", "Expecgender-", "pivotgender", "Explorogender", "Faegender", "Fascigender", "Faunagender", "Fawngender", "Felisgender", "Femfluid", "venufluid", "Femgender", "femme", "Firegender", "Fissgender", "Flirtgender", "amogender", "genderamas", "Flowergender", "diurnalgender", "Fluidflux", "Foggender", "Frostgender", "freezegender", "Fuzzgender", "Gemelgender", "Gemigender", "Geminigender", "Genderale", "Genderamas", "flirtgender", "Genderblank", "Genderblur", "Gendercosm", "gendervoid", "Genderdormant", "Gendereaux", "Genderflora", "Genderflight", "Genderflow", "aquarigender", "Genderfluid", "Genderflux", "Genderfuzz", "Gendermaverick", "Gendernegative", "Gender-Neutral", "Genderplasma", "Genderpositive", "Genderpunk", "Genderqueer", "Gendersea", "Genderstrange", "Gendervague", "Gendervex", "gyragender", "Gendervoid", "voidgender", "Genderwitched", "Gendfleur", "Girlflux", "Glassgender", "Glimragender", "Glitchgender", "Gossagender", "Greengender", "Greygender", "Gyraboy", "Gyragender", "gendervex", "Gyragirl", "Healegender", "Heliogender", "Hemigender", "Horogender", "Hydrogender", "Hypogender", "Illusogender", "Impediogender-", "Imperigender", "Inersgender", "apagender", "Intergender", "Invisigender", "Iragender", "Jupitergender", "Juxera", "Kingender", "Kynigender", "Lamingender", "Leogender", "Lethargender", "apagender", "Leukogender", "Levigender", "Liberique", "Libragender", "libramasculine", "librafeminine", "Librafluid", "agenderflux.", "Lichtgender-", "Lipsigender", "Locugender", "evaisgender", "Lovegender", "Ludogender", "Lysigender", "Magigender", "Maringender", "nubilagender", "Marfluid", "mascfluid", "Mascfluid", "marfluid", "Mascugender", "Maverique", "Medeigender", "Melogender", "Mirrorgender", "Molligender", "Moongender", "nocturnalgender", "Mosaigender-", "portiogender", "Musicgender", "Mutaregender", "Mutogender", "Mystigender", "Nanogender", "nan0gender", "Narkissigender", "Necrogender", "Nesciogender", "Neurogender", "Neutrois", "Nobifluid", "Nocturnalgender", "batgender", "owlgender", "moongender", "Non-binary", "Novigender", "Nubilagender", "maringender.", "Nullgender", "Nyctogender", "Obruogender", "Offgender", "Omnigay", "Orbgender", "Owlgender", "nocturnalgender", "Paragender", "Pendogender", "Perigender", "Perogender", "Personagender", "Perospike", "Pictogender-", "Pixelgender", "Polygender", "Polygenderflux", "Portiogender", "mosaigender", "Praegender", "Preciogender", "Preterbinary", "Primusgender", "Privagender", "Proxvir", "Quivergender", "Quoigender", "Salugender", "Schrodigender", "Scorigender", "Scorpifluid", "Scorpigender", "Seagender", "Selenogender", "monagender", "monegender.", "Sequigender", "Shellgender", "Skygender", "Spesgender", "Spikegender", "burstgender", "Stargender", "Staticgender", "Stratogender", "Subgender", "Subfluid", "Surgender", "Swampgender", "boggender", "Sychnogender", "Systemfluid", "Systemgender", "Tachigender", "Tangender", "Tauragender", "Technogender", "Telegender", "Tempgender", "Temporagender", "Tenuigender", "Tragender", "Traumatgender", "Trigender", "Turbogender", "Ungender", "antigender", "Vaguefluid", "Vagueflux", "Vaguegender", "Vapogender", "Vectorgender", "Veloxigender", "Venngender", "Venufluid", "femfluid", "Verangender", "Vestigender", "Vibragender", "Videgender", "aesthetgender", "Videogender", "Virgegender", "Vocigender", "Voidfluid", "Voidgender", "gendervoid", "Witchgender", "Xenogender", "Xirl", "Xoy", "Xumgender", "Zodiacgender"] 
        for gender in genders: 
            await ctx.send(gender)    
     
    @commands.is_owner()
    @commands.command(name="eval", aliases=["e", "ev", "evaluate"])
    async def eval_command(self, ctx, *, cmd):
        await ctx.message.add_reaction("🆗")
        await ctx.message.add_reaction("🇧")
        await ctx.message.add_reaction("🇴")
        await ctx.message.add_reaction("🅾")
        await ctx.message.add_reaction("🇲")
        await ctx.message.add_reaction("🇪")
        await ctx.message.add_reaction("🇷")
        """Evaluates input.
            Input is interpreted as newline seperated statements.
            If the last statement is an expression, that is the return value.
            Usable globals:
              - `bot`: the bot instance
              - `discord`: the discord module
              - `commands`: the discord.ext.commands module
              - `ctx`: the invocation context
              - `__import__`: the builtin `__import__` function
            Such that `>eval 1 + 1` gives `2` as the result.
            The following invocation will cause the bot to send the text '9'
            to the channel of invocation and return '3' as the result of evaluating
            >eval ```
            a = 1 + 2
            b = a * 2
            await ctx.send(a + b)
            a
            ```
        """
        fn_name = "_eval_expr"

        cmd = cmd.strip("` ")

        # add a layer of indentation
        cmd = "\n".join(f"    {i}" for i in cmd.splitlines())

        # wrap in async def body
        body = f"async def {fn_name}():\n{cmd}"

        parsed = ast.parse(body)
        body = parsed.body[0].body

        insert_returns(body)

        env = {
            'bot': ctx.bot,
            'discord': discord,
            'commands': commands,
            'ctx': ctx,
            'aiohttp': aiohttp,
            '__import__': __import__
        }
        exec(compile(parsed, filename="<ast>", mode="exec"), env)

        result = (await eval(f"{fn_name}()", env))
        await ctx.send(f"```\n\n{result}\n\n```")
