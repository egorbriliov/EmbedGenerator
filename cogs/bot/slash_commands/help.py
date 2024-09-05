import disnake
from disnake.ext import commands

embeds_dict = {
    0: {
        'embed': {
            'fields': [{'name': 'First steps', 'value': 'To get started, you need to use /embed', 'inline': False}],
            'image': {
                'url': 'https://media.discordapp.net/attachments/1262719342500384861/1263953249317158925'
                       '/chrome_kLpriNSOYs.gif?ex=669cc471&is=669b72f1&hm'
                       '=1ee7a00ba18ec13806ba67345c2641a614297018c603282b0d758b0dc0d08c19&=&width=657&height=314'}},
        'url': 'https://discord.com/channels/1263045771067002941/1263045771511726142/1263961169102766140'},
    1: {'embed': {
        'fields': [
            {'name': 'Add something',
             'value': 'To add something, you need to click a button and fill out the modal window',
             'inline': False}], 'image': {
            'url': 'https://media.discordapp.net/attachments/1262719342500384861/1263953248507658240/chrome_c3lv00QRtE'
                   '.gif?ex=669cc471&is=669b72f1&hm=8e1c5511664041c4305e154478edac16514df527a4e3e1342998a19536caad5b'
                   '&=&width=657&height=314'}},
        'url': 'https://discord.com/channels/1263045771067002941/1263045771511726142/1263961384152989707'},
    2: {'embed': {'fields': [
        {'name': 'Delete something',
         'value': 'To delete something, you need to click a button',
         'inline': False}], 'image': {
        'url': 'https://media.discordapp.net/attachments/1262719342500384861/1263953248927092869'
               '/chrome_dD06gFqCWc.gif?ex=669cc471&is=669b72f1&hm'
               '=1edf969222a076794162a38d5ca7f92824a6940b3f6ae23ebb054172fc251dc6&=&width=657&height=314'}},
        'url': 'https://discord.com/channels/1263045771067002941/1263045771511726142/1263961527338274828'},
    3: {'embed': {
        'fields': [{'name': 'Send embed',
                    'value': 'To send embed, you need to click button and choose method for send. If you choose “Send '
                             'this channel”, embed will be sent in this channel.\n',
                    'inline': False}],
        'image': {
            'url': 'https://media.discordapp.net/attachments/1262719342500384861/1263953248038158436'
                   '/chrome_6f1YRGIFE2.gif?ex=669cc471&is=669b72f1&hm'
                   '=11ffb597309a4a4e7260dbd3f274ef55b276d37f21e67bd2484216bbec143c02&=&width=657&height=314'},
        'footer': {"text": "You can go url source and find another method!",
                   "icon_url": ""}
    },
        'url': 'https://discord.com/channels/1263045771067002941/1263045771511726142/1263961763032862864',
    },
    4: {'embed': {'fields': [{'name': 'Input errors',
                              'value': 'You don’t have to worry about data entry errors, because if they '
                                       'are not true, <@1261557247113166859> will warn you!',
                              'inline': False}], 'image': {
        'url': 'https://media.discordapp.net/attachments/1262719342500384861/1263953250407940096'
               '/chrome_Y6D5l3lD51.gif?ex=669cc472&is=669b72f2&hm'
               '=e2b35beeb48287f08a0670793d3e2f1549ccef395578b494b5efd36915e83812&=&width=657&height=314'}},
        'url': 'https://discord.com/channels/1263045771067002941/1263045771511726142/1263962306958856223'}}


class ButtonGenerator(disnake.ui.Button):
    def __init__(self, bot, button_type, current_page):
        self.bot = bot
        self.button_type = button_type
        self.current_page = current_page
        if button_type == "previous_page":
            if current_page == 0:
                super().__init__(
                    label="<",
                    disabled=True,
                    style=disnake.ButtonStyle.grey,
                    row=1
                )
            else:
                super().__init__(
                    label="<",
                    disabled=False,
                    style=disnake.ButtonStyle.grey,
                    row=1
                )
        elif button_type == "current_page":
            super().__init__(
                label=f"Current step source",
                disabled=False,
                style=disnake.ButtonStyle.url,
                url=embeds_dict[self.current_page]["url"],
                row=1
            )
        elif button_type == "next_page":
            if current_page == len(embeds_dict) - 1:

                super().__init__(
                    label=">",
                    disabled=True,
                    style=disnake.ButtonStyle.grey,
                    row=1
                )
            else:
                super().__init__(
                    label=">",
                    disabled=False,
                    style=disnake.ButtonStyle.grey,
                    row=1
                )

    async def callback(self, interaction: disnake.Interaction):
        """
        Функция, которая будет вызываться при нажатии на кнопку.
        """
        if self.button_type == "previous_page":
            await interaction.response.edit_message(view=MyView(bot=self.bot, current_page=(self.current_page - 1)),
                                                    embed=disnake.Embed.from_dict(
                                                        embeds_dict[(self.current_page - 1)]["embed"]))
        elif self.button_type == "next_page":
            await interaction.response.edit_message(view=MyView(bot=self.bot, current_page=(self.current_page + 1)),
                                                    embed=disnake.Embed.from_dict(
                                                        embeds_dict[(self.current_page + 1)]["embed"]))


class MyView(disnake.ui.View):
    def __init__(self, bot, current_page):
        super().__init__(timeout=None)
        self.bot = bot
        self.current_page = current_page
        self.add_item(ButtonGenerator(button_type="previous_page", current_page=self.current_page, bot=self.bot))
        self.add_item(ButtonGenerator(button_type="current_page", current_page=self.current_page, bot=self.bot))
        self.add_item(ButtonGenerator(button_type="next_page", current_page=self.current_page, bot=self.bot))


class Help(commands.Cog):
    # Конструкция (bot : commands) здесь, чтобы дать IDE представление о том, какой тип данных содержит аргумент.
    # Это не обязательно, но может быть полезно при разработке.

    def __init__(self, bot: commands.Bot) -> None:
        """
        Метод инициализирует, бота, чтобы был доступ к боту
        """
        self.bot = bot

    @commands.slash_command(name="help", description="Shows examples of usage /embed")
    async def help(self,
                   inter: disnake.ApplicationCommandInteraction
                   ):
        await inter.response.send_message(view=MyView(bot=self.bot, current_page=0),
                                          embed=disnake.Embed.from_dict(
                                              embeds_dict[0]["embed"]),
                                          ephemeral=True)


def setup(bot: commands.Bot):
    """
    Авторизует бота в когах
    """
    bot.add_cog(Help(bot))
