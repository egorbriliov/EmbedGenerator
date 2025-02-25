import datetime
import validators

import disnake
from aiogram.client.session import aiohttp
from disnake.ext import commands

from PIL import Image
import requests
from io import BytesIO


class SendSelectMenu(disnake.ui.View):

    def __init__(self, embed_dict, bot):
        super().__init__()
        self.bot = bot
        self.embed_dict = embed_dict

    @disnake.ui.select(
        placeholder="Выберите вариант",
        min_values=1,
        max_values=1,
        options=[
            disnake.SelectOption(label="Use webhook", value="webhook"),
            disnake.SelectOption(label="Send this channel", value="channel"),
            disnake.SelectOption(label="Cancel", value="cancel"),
        ]
    )
    async def my_select(self, select: disnake.ui.Select, interaction: disnake.Interaction):

        if select.values[0] == "cancel":
            await interaction.response.edit_message("Creation was canceled",
                                                    components=None,
                                                    embed=None)
            await interaction.delete_original_response(delay=5)
        elif select.values[0] == "channel":
            await interaction.response.edit_message("Embed was sent", components=None, embed=None)
            await interaction.delete_original_response(delay=5)
            await interaction.channel.send(embed=disnake.Embed.from_dict(self.embed_dict))
        elif select.values[0] == "webhook":
            await interaction.response.send_modal(ModalGenerator(embed_dict=self.embed_dict,
                                                                 setting_name="webhook", bot=self.bot))


class ModalGenerator(disnake.ui.Modal):
    """
    Отвечает за:
    1) Создание модульного окна для получения нового названия для пользователя
    2) Установку нового названия для комнаты
    """

    def __init__(self, embed_dict: dict, setting_name: str, bot):
        self.bot = bot
        self.setting_name = setting_name
        self.embed_dict = embed_dict
        if setting_name in ["description", "title"]:
            if setting_name == "description":
                style = disnake.TextInputStyle.long
            else:
                style = disnake.TextInputStyle.short
            components = [
                disnake.ui.TextInput(label=self.setting_name.title(),
                                     placeholder=f"Enter embed {self.setting_name}",
                                     custom_id=setting_name,
                                     required=True,
                                     style=style)
            ]
        elif setting_name == "image":
            components = [
                disnake.ui.TextInput(label="Image url",
                                     placeholder=f"Enter image url",
                                     custom_id="url",
                                     required=True)]
        elif setting_name == "thumbnail":
            components = [
                disnake.ui.TextInput(label="Thumbnail url",
                                     placeholder=f"Enter thumbnail url",
                                     custom_id="url",
                                     required=True)]
        elif setting_name == "color":
            components = [
                disnake.ui.TextInput(label="Color Name",
                                     placeholder=f"Enter hex like as 0x123abc",
                                     custom_id="color",
                                     required=True)]
        elif setting_name == "author":
            components = [
                disnake.ui.TextInput(label="Author name",
                                     placeholder=f"Enter author name",
                                     custom_id="name",
                                     required=True),
                disnake.ui.TextInput(label="Author url",
                                     placeholder=f"Enter author url",
                                     custom_id="url",
                                     required=False),
                disnake.ui.TextInput(label="Author icon url",
                                     placeholder=f"Enter author icon url",
                                     custom_id="icon_url",
                                     required=False)
            ]
        elif setting_name == "footer":
            components = [
                disnake.ui.TextInput(label="Footer text",
                                     placeholder=f"Enter footer text",
                                     custom_id="text",
                                     required=True),
                disnake.ui.TextInput(label="Icon url",
                                     placeholder=f"Enter icon url",
                                     custom_id="icon_url",
                                     required=False)
            ]
        elif setting_name == "fields":
            components = [
                disnake.ui.TextInput(label="Field name",
                                     placeholder=f"Enter field name",
                                     custom_id="name",
                                     required=True),
                disnake.ui.TextInput(label="Field value",
                                     placeholder=f"Enter field value",
                                     custom_id="value",
                                     required=False,
                                     style=disnake.TextInputStyle.long),
                disnake.ui.TextInput(label="Field inline?",
                                     placeholder=f"True or False",
                                     custom_id="inline",
                                     required=False)
            ]
        elif setting_name == "webhook":
            components = [
                disnake.ui.TextInput(label=self.setting_name.title(),
                                     placeholder=f"Enter {self.setting_name}",
                                     custom_id=setting_name,
                                     required=True)
            ]
        else:
            components = []
        super().__init__(title=f'New {self.setting_name.title()}', components=components, custom_id=self.setting_name)

    async def callback(self, interaction: disnake.ModalInteraction):
        async def add_good():
            await interaction.response.edit_message(embed=disnake.Embed.from_dict(self.embed_dict),
                                                    view=MyView(self.embed_dict, bot=self.bot))
            await interaction.send(f"{self.setting_name.title()} has been update", delete_after=5, ephemeral=True)

        def is_valid_image_url(url):
            try:
                response = requests.get(url)
                img = Image.open(BytesIO(response.content))
                return True
            except:
                return False

        def is_valid_url(text):
            return validators.url(text)

        if self.setting_name in ["description", "title"]:
            setting_name = interaction.text_values[self.setting_name]
            self.embed_dict[self.setting_name] = setting_name
            await add_good()
        elif self.setting_name == "color":
            def is_valid_hex_str(hex_str):
                """
                If hex correct return int(hex)
                Else return False
                """
                try:
                    # Attempt to convert the string to an integer with base 16 (hexadecimal)
                    int(hex_str, 16)
                    return int(hex_str, 16)
                except ValueError:
                    return False

            if is_valid_hex_str(interaction.text_values[self.setting_name]):
                self.embed_dict["color"] = is_valid_hex_str(interaction.text_values[self.setting_name])
                await add_good()
            else:
                await interaction.send("Not correct color HEX. Hex format must be 0x123abc!",
                                       delete_after=5,
                                       ephemeral=True)
        elif self.setting_name == "footer":
            if interaction.text_values["icon_url"]:
                if is_valid_image_url(interaction.text_values["icon_url"]):
                    self.embed_dict[self.setting_name] = interaction.text_values
                    await add_good()
                else:
                    await interaction.send(f"You need past correct icon url!", delete_after=5,
                                           ephemeral=True)
            else:
                self.embed_dict[self.setting_name] = interaction.text_values
                await add_good()
        elif self.setting_name == "author":
            if interaction.text_values["icon_url"] and interaction.text_values["url"]:
                if is_valid_image_url(interaction.text_values["icon_url"]) and is_valid_url(
                        interaction.text_values["url"]):
                    self.embed_dict[self.setting_name] = interaction.text_values
                    await add_good()
                elif is_valid_image_url(interaction.text_values["icon_url"]) and not is_valid_url(
                        interaction.text_values["url"]):
                    await interaction.send(f"You need past correct author url!", delete_after=5,
                                           ephemeral=True)
                elif not is_valid_image_url(interaction.text_values["icon_url"]) and is_valid_url(
                        interaction.text_values["url"]):
                    await interaction.send(f"You need past correct icon url!", delete_after=5,
                                           ephemeral=True)
                elif not is_valid_image_url(interaction.text_values["icon_url"]) and not is_valid_url(
                        interaction.text_values["url"]):
                    await interaction.send(f"You need past correct author url and icon url!", delete_after=5,
                                           ephemeral=True)

            elif interaction.text_values["icon_url"] and not interaction.text_values["url"]:
                if is_valid_image_url(interaction.text_values["icon_url"]):
                    self.embed_dict[self.setting_name] = interaction.text_values
                    await add_good()
                elif not is_valid_image_url(interaction.text_values["icon_url"]):
                    await interaction.send(f"You need past correct icon url!", delete_after=5,
                                           ephemeral=True)
            elif not interaction.text_values["icon_url"] and interaction.text_values["url"]:
                if is_valid_image_url(interaction.text_values["url"]):
                    self.embed_dict[self.setting_name] = interaction.text_values
                    await add_good()
                elif not is_valid_image_url(interaction.text_values["url"]):
                    await interaction.send(f"You need past correct author url!", delete_after=5,
                                           ephemeral=True)
        elif self.setting_name in ["thumbnail", "image"]:
            if interaction.text_values["url"] and is_valid_image_url(interaction.text_values["url"]):
                self.embed_dict[self.setting_name] = {"url": interaction.text_values["url"]}
                await interaction.response.edit_message(embed=disnake.Embed.from_dict(self.embed_dict),
                                                        view=MyView(self.embed_dict, bot=self.bot))
            else:
                await interaction.send(f"You need past correct url!", delete_after=5,
                                       ephemeral=True)
        elif self.setting_name == "fields":
            data = interaction.text_values
            try:
                fields_name_list = [field.get("name") for field in self.embed_dict["fields"]]
            except:
                fields_name_list = []
            if data["name"] not in fields_name_list:
                if data["value"] or data["name"]:
                    if not data["inline"]:
                        data["inline"] = False
                    if self.embed_dict.get("fields"):
                        self.embed_dict["fields"].append(data)
                    else:
                        self.embed_dict["fields"] = [data]
                    try:
                        await interaction.response.edit_message(embed=disnake.Embed.from_dict(self.embed_dict),
                                                                view=MyView(self.embed_dict, bot=self.bot))
                    except Exception:
                        pass
                else:
                    await interaction.send(f"You need to pass value or name!", delete_after=5,
                                           ephemeral=True)
            else:
                await interaction.send(f"This name is already in use!", delete_after=5, ephemeral=True)
        elif self.setting_name == "webhook":
            try:
                webhook_url = interaction.text_values[self.setting_name]
                async with aiohttp.ClientSession() as webhook:
                    webhook = disnake.Webhook.from_url(url=webhook_url, session=webhook)
                    await webhook.send(embed=disnake.Embed.from_dict(self.embed_dict))
                    await interaction.response.edit_message(f"Embed was sent", components=None, embed=None)
            except Exception:
                await interaction.response.edit_message("How do you want to send embed?",
                                                        view=SendSelectMenu(self.embed_dict, bot=self.bot),
                                                        embed=None)
                await interaction.send(f"You need past correct url!", delete_after=5,
                                       ephemeral=True)


class ButtonGenerator(disnake.ui.Button):
    def __init__(self, embed_dict: dict, setting_name: str, value: int, setting_list: list, bot):
        self.embed_dict = embed_dict
        self.setting_name = setting_name
        self.row = value // 5
        self.bot = bot

        if setting_name in embed_dict and setting_name != "fields":
            super().__init__(
                label=setting_name.title(),
                style=disnake.ButtonStyle.red,
                row=self.row
            )

        elif setting_name in ["timestamp", "color"]:
            if embed_dict:
                super().__init__(
                    label=setting_name.title(),
                    style=disnake.ButtonStyle.green,
                    disabled=False,
                    row=self.row
                )
            else:
                super().__init__(
                    label=setting_name.title(),
                    style=disnake.ButtonStyle.green,
                    disabled=True,
                    row=self.row
                )

        elif setting_name not in embed_dict and setting_name in setting_list and setting_name != "send":
            super().__init__(
                label=setting_name.title(),
                style=disnake.ButtonStyle.green,
                row=self.row)

        elif setting_name == "fields":
            if self.embed_dict.get("fields"):
                if len(self.embed_dict.get("fields")) < 15:
                    super().__init__(
                        label=setting_name.title(),
                        style=disnake.ButtonStyle.green,
                        disabled=False,
                        row=self.row
                    )
                else:
                    super().__init__(
                        label=setting_name.title(),
                        style=disnake.ButtonStyle.green,
                        disabled=True,
                        row=self.row
                    )
            else:
                super().__init__(
                    label=setting_name.title(),
                    style=disnake.ButtonStyle.green,
                    disabled=True,
                    row=self.row
                )

        elif setting_name == "send":
            if self.embed_dict:
                super().__init__(
                    label=setting_name.title(),
                    style=disnake.ButtonStyle.grey,
                    disabled=False,
                    row=self.row
                )
            else:
                super().__init__(
                    label=setting_name.title(),
                    style=disnake.ButtonStyle.grey,
                    disabled=True,
                    row=self.row
                )

        else:
            super().__init__(
                label=f"Field: {setting_name}",
                style=disnake.ButtonStyle.red,
                row=self.row
            )

    async def callback(self, interaction: disnake.Interaction):
        """
        Функция, которая будет вызываться при нажатии на кнопку.
        """
        if (self.setting_name not in self.embed_dict and self.setting_name != "send") or self.setting_name == "fields":
            # Могут добавляться и без description or title
            if self.setting_name in ['description', 'fields', 'thumbnail', 'author', 'footer', 'title', 'image']:
                await interaction.response.send_modal(ModalGenerator(embed_dict=self.embed_dict,
                                                                     setting_name=self.setting_name, bot=self.bot))
            # Не могут добавляться и без description or title
            elif self.setting_name in ["timestamp", "color"]:
                if self.setting_name == "timestamp":
                    self.embed_dict[self.setting_name] = datetime.datetime.now().isoformat()
                    await interaction.response.edit_message(embed=disnake.Embed.from_dict(self.embed_dict),
                                                            view=MyView(self.embed_dict, bot=self.bot))
                if self.setting_name == "color":
                    await interaction.response.send_modal(ModalGenerator(embed_dict=self.embed_dict,
                                                                         setting_name=self.setting_name,
                                                                         bot=self.bot))
            # Для всех прочих (fields): удаляет из данных и отсылает ответ
            elif self.setting_name:
                if "fields" in self.embed_dict:
                    if self.setting_name in [field.get("name") for field in self.embed_dict["fields"]]:
                        fields = self.embed_dict["fields"]
                        if len(fields) > 1:
                            for field in fields:
                                if self.setting_name == field.get("name"):
                                    fields.remove(field)
                                    self.embed_dict.update({"fields": fields})
                        elif len(fields) == 1:
                            del self.embed_dict["fields"]

                        if self.embed_dict:
                            await interaction.response.edit_message(
                                embed=disnake.Embed.from_dict(self.embed_dict),
                                view=MyView(self.embed_dict, bot=self.bot))
                        else:
                            await interaction.response.edit_message(
                                embed=None,
                                view=MyView(self.embed_dict, bot=self.bot))
                        # Ответ на взаимодействие
                        await interaction.send(f"{self.setting_name.title()} has been deleted", ephemeral=True,
                                               delete_after=5)
        # Чистка при нажатии кнопки
        elif self.setting_name in self.embed_dict and self.setting_name != "fields":
            del self.embed_dict[self.setting_name]
            if (len(self.embed_dict) == 1) and (self.embed_dict.get("timestamp") or self.embed_dict.get("color")):
                if self.embed_dict.get("timestamp"):
                    del self.embed_dict["timestamp"]
                elif self.embed_dict.get("color"):
                    del self.embed_dict["color"]
            elif (len(self.embed_dict) == 2) and self.embed_dict.get("timestamp") and self.embed_dict.get("color"):
                del self.embed_dict["timestamp"]
                del self.embed_dict["color"]
            if self.embed_dict:
                await interaction.response.edit_message(
                    embed=disnake.Embed.from_dict(self.embed_dict),
                    view=MyView(self.embed_dict, bot=self.bot))
            else:
                await interaction.response.edit_message(
                    embed=None,
                    view=MyView(self.embed_dict, bot=self.bot))
            await interaction.send(f"{self.setting_name.title()} has been deleted",
                                   ephemeral=True,
                                   delete_after=5)
        elif self.setting_name == "send":
            await interaction.response.edit_message("How do you want to send embed?",
                                                    view=SendSelectMenu(self.embed_dict, bot=self.bot),
                                                    embed=None)


class MyView(disnake.ui.View):
    def __init__(self, embed_dict, bot):
        super().__init__(timeout=10000)  # Таймаут для неактивной View - 60 секунд
        self.bot = bot
        self.embed_dict = embed_dict
        setting_list = ['title', 'description', 'author', 'image', 'footer', 'timestamp', 'color', 'send', 'thumbnail',
                        'fields']
        for setting_name in setting_list:
            value = setting_list.index(setting_name)
            self.add_item(ButtonGenerator(embed_dict=embed_dict, setting_name=setting_name,
                                          value=value, setting_list=setting_list, bot=self.bot))

        fields = embed_dict.get("fields")
        if fields:
            for i, field in enumerate(fields):
                value = len(setting_list) + i
                self.add_item(ButtonGenerator(embed_dict=embed_dict, setting_name=field.get("name"),
                                              value=value, setting_list=setting_list, bot=self.bot))


class EmbedGenerator(commands.Cog):
    # Конструкция (bot : commands) здесь, чтобы дать IDE представление о том, какой тип данных содержит аргумент.
    # Это не обязательно, но может быть полезно при разработке.

    def __init__(self, bot: commands.Bot) -> None:
        """
        Метод инициализирует, бота, чтобы был доступ к боту
        """
        self.bot = bot

    @commands.slash_command(name="embed", description="Embed creator")
    async def embed(self,
                    inter: disnake.ApplicationCommandInteraction
                    ):
        if inter.guild:
            required_permissions = [
                "view_channel",
                "send_messages",
                "embed_links",
                "attach_files"
            ]

            user_channel_permissions = inter.channel.permissions_for(inter.user)
            member_missing_permissions: list = [perm
                                                for perm in required_permissions
                                                if not getattr(user_channel_permissions, perm)]

            bot_member = inter.guild.get_member(inter.bot.user.id)
            bot_channel_permissions = inter.channel.permissions_for(bot_member)
            bot_missing_permissions: list = [perm
                                             for perm in required_permissions
                                             if not getattr(bot_channel_permissions, perm)]

            if not member_missing_permissions and not bot_missing_permissions:
                await inter.response.send_message(view=MyView(embed_dict={}, bot=self.bot), ephemeral=True)
            elif member_missing_permissions:
                await inter.response.send_message(f"**You missing permissions:** \n• "
                                                  f"{'\n• '.join(map(str, member_missing_permissions))}",
                                                  ephemeral=True, delete_after=10)
            elif bot_missing_permissions:
                print(bot_missing_permissions)
                await inter.response.send_message(f"**<@1261557247113166859> missing permissions:** \n• "
                                                  f"{'\n• '.join(map(str, bot_missing_permissions))}",
                                                  ephemeral=True, delete_after=5)
        else:
            await inter.response.send_message(view=MyView(embed_dict={}, bot=self.bot), ephemeral=True)


def setup(bot: commands.Bot):
    """
    Авторизует бота в когах
    """
    bot.add_cog(EmbedGenerator(bot))
