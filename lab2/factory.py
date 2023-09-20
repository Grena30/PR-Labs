from player import Player
import xml.etree.ElementTree as ET
import player_pb2 as PlayerList


class PlayerFactory:
    def to_json(self, players):
        '''
            This function should transform a list of Player objects into a list with dictionaries.
        '''

        json_list = []

        for player in players:
            json_list.append({
                "nickname": player.nickname,
                "email": player.email,
                "date_of_birth": player.date_of_birth.strftime("%Y-%m-%d"),
                "xp": player.xp,
                "class": player.cls
            })

        return json_list

    def from_json(self, list_of_dict):
        '''
            This function should transform a list of dictionaries into a list with Player objects.
        '''

        player_list = []

        for player in list_of_dict:
            nickname = player["nickname"]
            email = player["email"]
            date_of_birth = player["date_of_birth"]
            xp = player["xp"]
            cls = player["class"]
            player_list.append(Player(nickname, email, date_of_birth, xp, cls))

        return player_list

    def from_xml(self, xml_string):
        '''
            This function should transform a XML string into a list with Player objects.
        '''

        player_list = []
        root = ET.fromstring(xml_string)

        for player in root:
            nickname = player.find("nickname").text
            email = player.find("email").text
            date_of_birth = player.find("date_of_birth").text
            xp = int(player.find("xp").text)
            cls = player.find("class").text
            player_list.append(Player(nickname, email, date_of_birth, xp, cls))

        return player_list

    def to_xml(self, list_of_players):
        '''
            This function should transform a list with Player objects into a XML string.
        '''

        xml_string = ""
        xml_string += "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
        xml_string += "<data>\n"

        for player in list_of_players:
            date_format = player.date_of_birth.strftime("%Y-%m-%d")
            xml_string += " <player>\n"
            xml_string += f"    <nickname>{player.nickname}</nickname>\n"
            xml_string += f"    <email>{player.email}</email>\n"
            xml_string += f"    <date_of_birth>{date_format}</date_of_birth>\n"
            xml_string += f"    <xp>{player.xp}</xp>\n"
            xml_string += f"    <class>{player.cls}</class>\n"
            xml_string += " </player>\n"

        xml_string += "</data>\n"

        return xml_string

    def from_protobuf(self, binary):
        '''
            This function should transform a binary protobuf string into a list with Player objects.
        '''

        players_list = PlayerList.PlayersList()
        players_list.ParseFromString(binary)

        player_objects = []
        for proto_player in players_list.player:
            nickname = proto_player.nickname
            email = proto_player.email
            date_of_birth = proto_player.date_of_birth
            xp = proto_player.xp
            cls = proto_player.cls

            # Cls is given as an integer so we look for its corresponding string, Name : Value
            class_string_value = PlayerList.Class.Name(cls)
            player = Player(nickname, email, date_of_birth, xp, class_string_value)
            player_objects.append(player)

            return player_objects

    def to_protobuf(self, list_of_players):
        '''
            This function should transform a list with Player objects into a binary protobuf string.
        '''

        players_list = PlayerList.PlayersList()

        for player in list_of_players:
            player_object = players_list.player.add()
            player_object.nickname = player.nickname
            player_object.email = player.email
            player_object.date_of_birth = player.date_of_birth.strftime("%Y-%m-%d")
            player_object.xp = player.xp
            player_object.cls = player.cls

        protobuf_data = players_list.SerializeToString()
        return protobuf_data