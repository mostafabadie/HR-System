import sqlite3
import random
from datetime import datetime, timedelta

DB_PATH = "hr.db"

FIRST_NAMES = [
    "Ahmed","Mohamed","Mahmoud","Mostafa","Youssef","Omar","Ali","Ibrahim","Khaled","Hassan",
"Hussein","Tarek","Amr","Walid","Karim","Islam","Marwan","Hesham","Sherif","Ayman",
"Abdelrahman","Abdelaziz","Abdullah","Saeed","Hamdy","Magdy","Bassem","Adel","Nader","Tamer","Sameh","Wael","Hany","Shady","Fady",
"Ramy","Samir","Ashraf","Sabry","Lotfy","Zaki","Fouad","Gamal","Salah","Farouk",
"Reda","Ehab","Mamdouh","Nabil","Osama","Basel","Belal","Hazem","Moataz","Montaser","Shaban","Metwally","Eid","Nassar","Ashour",
"Hegazy","Salem","Bayoumi","Ghoneim","Zahran","Kamal","Ragab","Saad","Shawky","Sobhy",
"Yahia","Zakaria","Ismail","Anas","Hamza","Fares","Kareem","Laith","Mina","Bishoy","Rafik","Adham","Alaa","Bahaa","Badr",
"Diaa","Emad","Essam","Galal","Hatem","Helmy","Hossam","Khalil","Madgy","Maher",
"Medhat","Mido","Moez","Mokhtar","Naeem","Nagy","Nour","Raafat","Ragheb","Raheem","Ramadan","Rashad","Rasheed","Saber","Safwat",
"Samy","Sayed","Shaaban","Shaker","Shams","Shawer","Shehata","Shokr","Soliman","Talaat",
"Tawfik","Tharwat","Wagdy","Yasser","Younes","Sara","Fatma","Mariam","Aya","Nada","Salma","Heba","Rania","Yasmin","Reem",
"Malak","Shahd","Doaa","Eman","Hoda","Amira","Sahar","Hagar","Laila","Menna",
"Nesma","Rasha","Rawan","Riham","Ruba","Sama","Samar","Sondos","Tasneem","Walaa","Yomna","Zeinab","Abeer","Afaf","Alia",
"Amal","Amani","Asmaa","Ayaat","Azza","Basma","Dalia","Dina","Ebtisam","Faten",
"Ghada","Hala","Hanan","Hend","Iman","Inas","Iraa","Jana","Khadija","Lobna","Maha","Manal","Maram","Mervat","Mona",
"Nadine","Naglaa","Nahed","Nawal","Noha","Norhan","Ola","Radwa","Raniah","Rehab",
"Rokaya","Rubaida","Safaa","Sally","Samah","Sawsan","Shaimaa","Shereen","Soha","Suhair","Tahani","Wafaa","Yara","Yasmina","Zahraa",
"Zain","Zayd","Ziyad","Abanoub","Atef","Ateya","Ayoub","Barakat","Botros","Daoud",
"Elias","Fakhry","Faris","George","Gerges","Habib","Hafez","Halim","Hanna","Haroun","Issa","Karam","Khalaf","Labib","Lazar",
"Luka","Malek","Mansour","Mark","Mikhail","Mourad","Naseem","Nasr","Nehad","Nimr",
"Rafaat","Ramyh","Rizk","Samson","Selim","Stephanos","Tadros","Tawadros","Yacoub","Yehia","Yohanna","Zaher","Zidan","Zuhair","Abbas",
"Abed","Adnan","Afifi","Akel","Alfy","Aly","Ammar","Anwar","Aref","Asem",
"Asim","Atia","Awad","Awwad","Azmy","Badawi","Bakr","Barhoum","Bashar","Basyouni","Bassam","Botrosy","Dawood","Dorgham","Ezz",
"Ezzat","Fahmy","Fahim","Fahmyh","Fathi","Fathyh","Fawzi","Gaber","Gad","Ghaith",
"Ghazi","Hamdan","Hamdouh","Hamzaa","Hanyh","Harby","Hashim","Hassanein","Hatemh","Hisham","Hossny","Ibraheem","Idris","Imadh","Iyad",
"Jaber","Jalal","Jamalh","Jibril","Kamelh","Karamh","Khalifah","Khattab","Mahmoudh","Mahmoudy",
"Majed","Makram","Marouf","Masoud","Mesbah","Meteb","Minaah","Mokbel","Morsi","Mostafah","Nabhan","Nafea","Nagah","Nehme","Nesim",
"Nouh","Okasha","Qasim","Raed","Ragaa","Raghy","Raheel","Ramzi","Rashed","Rauf",
"Rifai","Saafan","Sabah","Sadeq","Saeedh","Sakr","Salamah","Saleh","Salimh","Samih","Sari","Sattar","Shaarawy","Shafik","Shalaby",
"Sharaf","Shehab","Shenouda","Shoukry","Siddiq","Subhi","Taher","Taha","Tamam","Thabet",
"Wadie","Wahid","Waseem","Yamani","Yasin","Younan","Youssefh","Yussry","Zaghloul","Zaherh","Zakiya","Zein","Zidanah","Zuhairy","Abdalmoneim",
"Abdelgawad","Abdelhadi","Abdelhakim","Abdelkader","Abdelkarim","Abdelkhalek","Abdellatif","Abdelmagid","Abdelmalek","Abdelnaby",
"Abdelrahim","Abdelraouf","Abdelsalam","Abdelsattar","Abdelwahab","Abouelenein","Abouzeid","Adawy","Adawyh","Afandy","Aggour","Alfyh","Arafa","Arafat","Arian",
"Asfour","Ashmawy","Attallah","Awadhi","Azzam","Badran","Bahgat","Bahnas","Bakheet","Balbaa",
"Barakaty","Bedeir","Bekhit","Beltagy","Bishara","Botrosan","Boutros","Daif","Darwish","Desouky","Doss","Ebeid","Eldeeb","Eldin","Elfeki",
"Elgamal","Elgendy","Elgohary","Elhaddad","Elhakeem","Elhamy","Elkashef","Elmasry","Elmenshawy","Elsafty",
"Elsayedh","Elsherbiny","Elsherif","Eltahawy","Eltantawy","Elwakeel","Elwan","Emarah","Fahd","Fahmyan","Fakhr","Farrag","Fathyah","Fawzyh","Gadallah",
"Gendy","Gergesy","Ghonim","Habashy","Hafezy","Hagag","Hagrass","Halaby","Hamada","Hammam",
"Hamoud","Hassaballah","Hassany","Hawary","Hegab","Helal","Hemdan","Henein","Herz","Hikal","Ibrahimy","Iskandar","Kandil","Karamallah","Kashif",
"Keshk","Khalifahh","Kholy","Khorshid","Labban","Lotfollah","Maghawry","Mahrous","Makhlouf","Mekky",
"Mikhael","Morcos","Naguib","Nasrallah","Shenawy" "Maryam", "Maryana", "Maryem", "Maryiam", "Marylu", "Maryse", "Masar",
"Mashael", "Mashal", "Masooma", "Masooma", "Mastoura", "Masturah",
"Masyoon", "Matin", "Maud", "Maura", "Mawada", "Mawaddah", "Mawiya",
    "Mawiya", "Maya", "Mayada", "Mayam", "Mayan", "Mayar", "Mayasa",
    "Maysoon", "Maysoon", "Mayy", "Mayyada", "Mayyadah", "Mazna", "Maznah",
    "Meera", "Mehak", "Mehr", "Mehrangiz", "Mehwish", "Mekka", "Mela",
    "Melanie", "Meliha", "Melina", "Melis", "Melisa", "Melissa", "Mena",
    "Meral", "Mercedes", "Merna", "Meroe", "Merv", "Merve", "Merveille",
    "Meryam", "Meryem", "Mesa", "Mia", "Miar", "Midya", "Mihad", "Mihera",
    "Mika", "Mikayla", "Mila", "Milagros", "Milani", "Milca", "Milena",
    "Milia", "Milica", "Milly", "Mina", "Minal", "Minana", "Mira", "Mirabelle",
    "Miral", "Miran", "Mireille", "Mirella", "Mirette", "Mirna", "Mirvat",
    "Misha", "Misk", "Misk", "Miski", "Miyah", "Mizna", "Moana", "Moazah",
    "Mobarakah", "Moe", "Moeena", "Moeza", "Moghira", "Mohra", "Moira",
    "Mojan", "Mona", "Monera", "Monica", "Monia", "Monia", "Monica",
    "Montaha", "Montaser", "Mora", "Mouna", "Mounia", "Mounira", "Mouruj",
    "Moutaz", "Mozah", "Mozna", "Mubaraka", "Mufida", "Muhjah", "Muhtaramah",
    "Mujahidah", "Mukarramah", "Mumina", "Mumtaz", "Muna", "Munaa", "Munirah",
    "Munisa", "Muntaha", "Muntaz", "Munya", "Murasil", "Murjanah", "Murshidah",
    "Muskaan", "Muslimah", "Muzna", "Muznah", "Mya", "Mysha", "Mystique",
    "Naama", "Naamah", "Naarah", "Nabaa", "Naba", "Nabeeha", "Nabeela",
    "Nabila", "Nabihah", "Nabiha", "Nabihah", "Nabiyah", "Nada", "Nadah",
    "Nadia", "Nadida", "Nadima", "Nadira", "Nadiya", "Nadiyah", "Nadwa",
    "Nadwah", "Nafeesa", "Nafeessa", "Nafesa", "Nafessa", "Nafisa", "Nafisah",
    "Nafsika", "Nagah", "Nagam", "Naghan", "Nagham", "Naghmeh", "Nagi", "Nagia",
    "Nagiba", "Nagla", "Naglaa", "Nagwa", "Nahaand", "Nahay", "Nahed", "Nahel",
    "Nahella", "Nahid", "Nahida", "Nahla", "Nahlah", "Nahom", "Nahrain",
    "Nahwan", "Naif", "Nailah", "Naima", "Naimah", "Najat", "Najati", "Najd",
    "Najda", "Najeya", "Naji", "Naji'a", "Najia", "Najiba", "Najibah", "Najila",
    "Najiyah", "Najla", "Najlaa", "Najma", "Najmah", "Najwa", "Najwan",
    "Nakeya", "Nakia", "Nakisa", "Nakita", "Nalaila", "Nalini", "Namariq",
    "Namira", "Nana", "Nancie", "Nancy", "Nane", "Nani", "Naomi", "Narain",
    "Narcisse", "Narda", "Nareeman", "Nargis", "Nargiza", "Nari", "Naria",
    "Nariman", "Narin", "Narjis", "Narmin", "Narmina", "Nashaat", "Nashat",
    "Nashida", "Nashira", "Nashita", "Nashmia", "Nashwa", "Nashwah", "Nasia",
    "Nasiba", "Nasibah", "Nasifa", "Nasifah", "Nasiha", "Nasikah", "Nasim",
    "Nasima", "Nasimah", "Nasira", "Nasirah", "Nasreen", "Nasrin", "Nassef",
    "Nassima", "Nassira", "Natalia", "Natalie", "Nataly", "Natasha", "Nathalie",
    "Nathera", "Nathifa", "Natiq", "Natira", "Natisha", "Nawal", "Nawar",
    "Nawara", "Nawaya", "Nawel", "Nawwar", "Nawwara", "Naya", "Nayab", "Nayel",
    "Nayla", "Naylah", "Nayra", "Nayyab", "Nayyirah", "Nazanine", "Nazek",
    "Nazeem", "Nazha", "Nazia", "Naziha", "Nazik", "Nazila", "Nazira", "Nazirah",
    "Nazish", "Naziyah", "Nazli", "Nazly", "Nazma", "Nazneen", "Nazy", "Ndala",
    "Ne'ma", "Neamat", "Neama", "Neamat", "Neda", "Nedaa", "Nedal", "Neelam",
    "Neelofar", "Neema", "Neena", "Nefertari", "Nefertiti", "Nehal", "Nehaya",
    "Nehed", "Nehmat", "Nejla", "Nelly", "Nemat", "Nematallah", "Nemer", "Nemira",
    "Nena", "Neola", "Nephthys", "Neptis", "Nermeen", "Nermin", "Nermina",
    "Nesma", "Nesma", "Nesreen", "Nessma", "Nessrin", "Nevien", "Nevin",
    "Nevine", "Neyla", "Nezar", "Nezha", "Nga", "Ngoc", "Ngozi", "Ni'ma",
    "Ni'maa", "Nia", "Niaa", "Niamh", "Nibal", "Nibras", "Nicole", "Nidal",
    "Nidya", "Nihad", "Nihal", "Nija", "Nijma", "Nikita", "Nikki", "Niko",
    "Nikola", "Nila", "Nile", "Nilia", "Nima", "Nimat", "Nimet", "Nimira",
    "Nina", "Nina", "Ninar", "Ninel", "Nini", "Ninia", "Ninorta", "Niobe",
    "Nipuna", "Nirmeen", "Nirmeen", "Nisreen", "Nisrin", "Nissa", "Nissma",
    "Niveen", "Niven", "Nivin", "Niwars", "Niya", "Niyazi", "Nizana", "Noa",
    "Noah", "Noel", "Noelle", "Noemi", "Noha", "Nohad", "Noor", "Nooreyah",
    "Nooreyeh", "Noosha", "Nora", "Norah", "Noralba", "Noran", "Norcen",
    "Norcen", "Norhan", "Nori", "Noria", "Noriana", "Norien", "Norin", "Norine",
    "Noris", "Nosa", "Nosha", "Noura", "Nourah", "Nouran", "Nourhan", "Nouri",
    "Nouria", "Nourian", "Nourine", "Nourya", "Nova", "Novia", "Nour", "Nubia",
    "Nuda", "Nudar", "Nudhar", "Nuf", "Nufaysa", "Nuhad", "Nujaim", "Nujood",
    "Numa", "Nuna", "Nura", "Nurah", "Nuran", "Nurbai", "Nurhan", "Nuri", "Nuria",
    "Nurian", "Nurit", "Nurten", "Nusayba", "Nusaybah", "Nusayb", "Nusrat",
    "Nusrat", "Nuwair", "Nuwar", "Nuwayr", "Nuzha", "Nuzhat", "Nyala", "Nyla",
    "Nyle", "Nyla", "Nymph", "Nyra", "Nyree", "Nysa", "Nyx", "Nyz", "Obaida",
    "Obaidah", "Obaidat", "Obaidullah", "Obay", "Obaya", "Obayda", "Obeida",
    "Obeidah", "Obeidat", "Obeir", "Obey", "Obeyd", "Obeyda", "Obeydah", "Oceana",
    "Oceane", "October", "Odalis", "Odalys", "Oda", "Ode", "Odeh", "Odelet",
    "Odeleth", "Odell", "Odella", "Odelle", "Odera", "Odet", "Odetta", "Odette",
    "Odetty", "Odila", "Odile", "Odilia", "Odin", "Odo", "Odon", "Odona",
    "Odyssa", "Odysse", "Odyssey", "Ofa", "Ofa", "Ofak", "Ofelia", "Ofeliah",
    "Ofeq", "Ofira", "Ofra", "Oft", "Og", "Oga", "Ogar", "Ogden", "Oge", "Ogen",
    "Ogenya", "Ogg", "Ogi", "Ogima", "Ogla", "Ogle", "Ogma", "Ogra", "Oguz",
    "Ohan", "Ohanna", "Ohanne", "Ohel", "Ohela", "Ohelah", "Ohelen", "Ohella",
    "Ohera", "Ohiana", "Ohini", "Ohma", "Ohmd", "Ohna", "Ohndrea", "Ohndreea",
    "Ohndreia", "Ohndreya", "Ohndria", "Ohndriah", "Ohndriana", "Ohndrianna",
    "Ohndriannah", "Ohndrie", "Ohndrielle", "Ohndrina", "Ohndrine", "Ohndrya",
    "Ohndryah", "Ohndryana", "Ohndryanna", "Ohndryannah", "Ohndrye", "Ohndryelle",
    "Ohndryna", "Ohndryne", "Ohndrya", "Ohndryah", "Ohndryana", "Ohndryanna",
    "Ohndryannah", "Ohndrye", "Ohndryelle", "Ohndryna", "Ohndryne", "Ohndrya",
    "Ohndryah", "Ohndryana", "Ohndryanna", "Ohndryannah", "Ohndrye", "Ohndryelle",
    "Ohndryna", "Ohndryne", "Ohni", "Ohnia", "Ohnora", "Ohnore", "Ohnri", "Ohnria",
    "Ohnriah", "Ohnriana", "Ohnrianna", "Ohnriannah", "Ohnrie", "Ohnrielle",
    "Ohnrina", "Ohnrine", "Ohnrya", "Ohnryah", "Ohnryana", "Ohnryanna", "Ohnryannah",
    "Ohnrye", "Ohnryelle", "Ohnryna", "Ohnryne", "Ohnrya", "Ohnryah", "Ohnryana",
    "Ohnryanna", "Ohnryannah", "Ohnrye", "Ohnryelle", "Ohnryna", "Ohnry""Kalthoom", "Kamaliyah", "Kamilah", "Kanar", "Kanza", "Karima", "Karine",
    "Karma", "Karolina", "Katherine", "Kawthar", "Kayan", "Kayla", "Kazimah",
    "Kenda", "Kenzy", "Kenza", "Khadija", "Khadijah", "Khair", "Khairat",
    "Khairia", "Khairiyah", "Khalida", "Khalilah", "Khalisah", "Khalood",
    "Khawla", "Khayriah", "Khazna", "Khulood", "Khulud", "Khushboo",
    "Kifah", "Kinda", "Kinza", "Kulthum", "Laila", "Lamees", "Lamis",
    "Lamya", "Lamyaa", "Lana", "Lara", "Lareen", "Larene", "Larina",
    "Larissa", "Latifa", "Lava", "Layan", "Layla", "Laylaa", "Layyah",
    "Lea", "Leena", "Leila", "Lena", "Leyla", "Lina", "Linda", "Lobna",
    "Lojain", "Lora", "Loreen", "Loren", "Lorraine", "Lotus", "Loubna",
    "Loulwa", "Louna", "Lubaba", "Lubna", "Lujain", "Lujaina", "Luma",
    "Luna", "Luri", "Lutfiya", "Lynn", "Maha", "Mahasen", "Mahasin", "Mahek",
    "Maher", "Mahira", "Mahitab", "Mahmood", "Mahmoud", "Mahra", "Mahreen",
    "Mai", "Maida", "Mairam", "Maire", "Mais", "Maisa", "Maisam", "Maisoon",
    "Maissa", "Maisoon", "Maiwand", "Majda", "Majdah", "Majeeda", "Majida",
    "Majidah", "Makarem", "Malak", "Malakah", "Malika", "Malikah", "Manaal",
    "Manahil", "Manal", "Manar", "Manawwar", "Mandira", "Maneh", "Mansurah",
    "Manuela", "Mara", "Marah", "Maram", "Marcel", "Marcelle", "Mardhiyah",
    "Mari", "Maria", "Mariam", "Mariana", "Marie", "Mariella", "Mariem",
    "Marija", "Mariya", "Mariyah", "Mariz", "Marj", "Marjani", "Marjem",
    "Marlo", "Marlyn", "Marnie", "Maroa", "Mars", "Marsha", "Marsil",
    "Marta", "Martha", "Marwa", "Marwah", "Mary", "Marya", "Maryah"
]
LAST_NAMES = [
    "Hassan","Ibrahim","Mahmoud","Ali","Mostafa","Abdelrahman","Abdelaziz","Abdullah","Elsayed","Farouk",
"Soliman","Gamal","Salah","Hamdan","Zaki","Fathy","Kamel","Ragab","Saad","Shaban",
"Metwally","Eid","Nassar","Fouad","Mansour","Sabry","Ashour","Khalifa","Badawy","Hegazy","Salem","Lotfy","Reda","Shawky","Zahran",
"Ghoneim","Bayoumi","Hafez","Helal","Hemdan","Henein","Herz","Hikal","Iskandar","Kandil",
"Karam","Kashif","Keshk","Khalil","Khorshid","Labban","Magdy","Mahrous","Makhlouf","Mekky","Mikhael","Morcos","Naguib","Nasrallah","Shenawy",
"Abdelgawad","Abdelhadi","Abdelhakim","Abdelkader","Abdelkarim","Abdelkhalek","Abdellatif","Abdelmagid","Abdelmalek","Abdelnaby",
"Abdelrahim","Abdelraouf","Abdelsalam","Abdelsattar","Abdelwahab","Abouelenein","Abouzeid","Adawy","Aggour","Arafa","Arafat","Arian","Asfour","Ashmawy","Attallah",
"Azzam","Badran","Bahgat","Bahnas","Bakheet","Balbaa","Barakaty","Bedeir","Bekhit","Beltagy",
"Bishara","Boutros","Darwish","Desouky","Doss","Ebeid","Eldeeb","Eldin","Elfeki","Elgamal","Elgendy","Elgohary","Elhaddad","Elhakeem","Elhamy",
"Elkashef","Elmasry","Elmenshawy","Elsafty","Elsherbiny","Elsherif","Eltahawy","Eltantawy","Elwakeel","Elwan",
"Emarah","Fahmy","Fakhr","Farrag","Gadallah","Gendy","Gergis","Ghonem","Habashy","Hafezy","Hagag","Hagrass","Halaby","Hamada","Hammam",
"Hamoud","Hassaballah","Hassany","Hawary","Hegab","Helmy","Hossam","Khalaf","Labib","Lazar",
"Luka","Malek","Mark","Mikhail","Mourad","Naseem","Nasr","Nehad","Nimr","Rafaat","Ramzi","Rashed","Rauf","Rifai","Saafan",
"Sadeq","Saleh","Salim","Samih","Sari","Sattar","Shaarawy","Shafik","Shalaby","Sharaf",
"Shehab","Shoukry","Siddiq","Subhi","Taher","Taha","Tamam","Thabet","Wadie","Wahid","Waseem","Yamani","Yasin","Younan","Yussry",
"Zaghloul","Zaher","Zein","Zidan","Zuhairy","Abbas","Abed","Adnan","Afifi","Akel",
"Aly","Ammar","Anwar","Aref","Asem","Asim","Atia","Awad","Azmy","Badawi","Bakr","Bashar","Bassam","Dawood","Dorgham",
"Ezz","Ezzat","Fahim","Fathi","Fawzi","Gaber","Gad","Ghaith","Ghazi","Hamdy",
"Harby","Hashim","Hassanein","Hatem","Hisham","Hossny","Idris","Imad","Iyad","Jaber","Jalal","Jibril","Kamal","Makram","Marouf",
"Masoud","Mesbah","Meteb","Mokbel","Morsi","Nabhan","Nafea","Nagah","Nehme","Nouh",
"Okasha","Qasim","Raed","Ragaa","Raghy","Raheel","Rizk","Samson","Selim","Stephanos","Tadros","Tawadros","Yacoub","Yehia","Yohanna",
"Zaherh","Zuhair","Abanoub","Atef","Ateya","Ayoub","Barakat","Botros","Daoud","Elias",
"Fakhry","Faris","George","Gerges","Habib","Halim","Hanna","Haroun","Issa","Karamy","Khalifah","Labibah","Maleky","Mansoury","Mourady",
"Naseemy","Nasry","Rafaty","Ramadan","Rasheed","Saber","Safwat","Samy","Sayed","Shaaban",
"Shaker","Shams","Shehata","Shokr","Soliman","Talaat","Tawfik","Tharwat","Wagdy","Yasser","Younes","Zakiya","Zeinab","Zidanah","Abdalmoneim",
"Abdelazeem","Abdelbaset","Abdeldaem","Abdelfadeel","Abdelghany","Abdelhamid","Abdeljaleel","Abdelmoneim","Abdelrazek","Abdelshafy",
"Abdeltawab","Abdelwahid","Abdelzaher","Abdelzeem","Abouhashim","Aboushady","Adelson","Aldin","Alfy","Amin","Aminy","Arafaah","Armanious","Asaad","Asham",
"Ashoury","Assaad","Attia","Awady","Ayady","Azab","Azhar","Bahy","Bahyeldin","Bakhit",
"Banna","Barhoum","Basyouny","Batta","Bedeiry","Bekheity","Beltagyy","Bishoy","Botrosy","Botrosan","Daif","Dawoudy","Desoky","Dorghamy","Eldeiry",
"Eldomyaty","Elfayoumy","Elhawary","Elhelaly","Elhusseiny","Elkhateeb","Elkholy","Elmahdy","Elminshawy","Elrashidy",
"Elsakka","Elsawy","Elsobky","Eltouny","Elzayat","Emam","Erian","Fahd","Fahmyan","Fathyah","Fawzyh","Gabr","Gadkarim","Gergesy","Ghonemy",
"Habashyah","Hafeez","Hagrasy","Hakim","Halwany","Hamouda","Hannaey","Hariry","Hassaney","Hawashy",
"Hegazyh","Helaly","Hemady","Heneiny","Hikalh","Ibrahimi","Iskandary","Kandily","Karimy","Kashify","Keshky","Khalify","Kholi","Khorshidi","Labbany",
"Lotfyh","Maghawry","Mahfouz","Mahmoudy","Makhloufy","Mekawy","Mikhaili","Morcosy","Naguiby","Nasrallahh",
"Rasheedy","Rizky","Sabahy","Sakr","Salamah","Salehy","Salimy","Samahy","Sariy","Sattary","Shaarawyy","Shafiky","Shalabyy","Sharafy","Shehaby",
"Shenoudy","Shoukryy","Siddiqy","Subhyy","Tahery","Tantawy","Thabeti","Wahby","Waseemy","Yassiny",
"Yehiany","Yohanny","Zaghlouly","Zahery","Zidaney","Zuhairyh","Abdelazimy","Abdelbary","Abdelghaffar","Abdelkarimy","Abdellah","Abdelmoaty","Abdelrazik","Abdelsabour","Abdelsayed",
"Abdelwahaby","Abouelkhair","Abouelnaga","Abouelnour","Adawyh","Aggoury","Arafaty","Ashmawyy","Attallahy","Azzamy",
"Badrany","Bahgaty","Bakheety","Barakatyy","Bedeiryh","Bekhity","Beltagyyh","Bisharay","Boutrosy","Darwishy",
"Desoukyy","Dossy","Ebeidy","Eldeeby","Elfeky","Elgendyy","Elgoharyy","Elhaddady","Elhamyy","Elkashefy","Badie","Elmezain"
]

EGYPT_GOVS = [
    "Cairo", "Giza", "Alexandria", "Qalyubia", "Sharqia", "Gharbia",
    "Dakahlia", "Beheira", "Kafr El-Sheikh", "Minya", "Sohag", "Assiut",
    "Aswan", "Luxor", "Beni Suef", "Fayoum", "Ismailia", "Port Said",
    "Suez", "Red Sea", "Matrouh", "North Sinai", "South Sinai",
]


def generate_fake_attendance(cur, employee_ids, days=30):
    """إنشاء حضور وانصراف عشوائي لعدد من الأيام الماضية لكل موظف"""
    today = datetime.today().date()
    for emp_id in employee_ids:
        for d in range(days):
            # احتمال حضور في هذا اليوم
            if random.random() < 0.7:
                day = today - timedelta(days=d)
                date_str = day.strftime("%Y-%m-%d")
                # وقت حضور بين 8 و10 صباحاً
                in_hour = random.randint(8, 10)
                in_min = random.randint(0, 59)
                check_in = f"{in_hour:02d}:{in_min:02d}:00"
                # وقت انصراف بين 15 و18 مساءً
                out_hour = random.randint(15, 18)
                out_min = random.randint(0, 59)
                check_out = f"{out_hour:02d}:{out_min:02d}:00"
                cur.execute(
                    """
                    INSERT INTO attendance (employee_id, date, check_in, check_out)
                    VALUES (?, ?, ?, ?)
                    """,
                    (emp_id, date_str, check_in, check_out),
                )


def rating_to_score(rating: str) -> float:
    mapping = {
        "ممتاز": 5.0,
        "جيد جداً": 4.0,
        "جيد": 3.0,
        "مقبول": 2.0,
        "ضعيف": 1.0,
    }
    return mapping.get(rating, 0.0)


def score_to_rating(score: float) -> str:
    if score >= 4.5:
        return "ممتاز"
    elif score >= 3.5:
        return "جيد جداً"
    elif score >= 2.5:
        return "جيد"
    elif score >= 1.5:
        return "مقبول"
    else:
        return "ضعيف"


def generate_fake_evaluations(cur, employee_ids):
    """إنشاء تقييمات أداء عشوائية للموظفين"""
    # الحصول على الفترات التقييمية
    periods = cur.execute("SELECT id FROM evaluation_periods").fetchall()
    if not periods:
        return  # لا توجد فترات، لا ننشئ تقييمات

    # الحصول على معايير التقييم
    criteria = cur.execute(
        "SELECT id, weight FROM evaluation_criteria WHERE is_active = 1"
    ).fetchall()
    if not criteria:
        return  # لا توجد معايير، لا ننشئ تقييمات

    ratings = ["ممتاز", "جيد جداً", "جيد", "مقبول", "ضعيف"]

    for emp_id in employee_ids:
        # احتمال أن هذا الموظف يكون له تقييم (مثلاً 60%)
        if random.random() > 0.6:
            continue

        period_id = random.choice(periods)[0]

        # عدم إنشاء أكثر من تقييم لنفس الموظف في نفس الفترة
        existing = cur.execute(
            """
            SELECT id FROM performance_evaluations
            WHERE employee_id = ? AND period_id = ?
            """,
            (emp_id, period_id),
        ).fetchone()
        if existing:
            continue

        total_score = 0.0
        total_weight = 0.0
        details = []

        for crit_id, weight in criteria:
            rating = random.choice(ratings)
            score = rating_to_score(rating)
            w = weight if weight is not None else 1.0
            total_score += score * w
            total_weight += w
            details.append((crit_id, rating, score))

        if total_weight == 0:
            continue

        overall_score = total_score / total_weight
        overall_rating = score_to_rating(overall_score)

        strengths = "أداء قوي في معظم المعايير."
        areas_for_improvement = "يمكن تحسين بعض المهارات."
        goals_next_period = "تطوير المهارات الفنية والالتزام بالمواعيد."
        comments = "تقييم وهمي لأغراض الاختبار."

        # إنشاء التقييم الرئيسي
        cur.execute(
            """
            INSERT INTO performance_evaluations
            (employee_id, period_id, evaluator_id, overall_rating, overall_score,
             strengths, areas_for_improvement, goals_next_period, comments, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                emp_id,
                period_id,
                1,  # مقيم افتراضي
                overall_rating,
                overall_score,
                strengths,
                areas_for_improvement,
                goals_next_period,
                comments,
                "completed",
            ),
        )
        eval_id = cur.lastrowid

        # تفاصيل التقييم
        for crit_id, rating, score in details:
            cur.execute(
                """
                INSERT INTO evaluation_details
                (evaluation_id, criteria_id, rating, score, comments)
                VALUES (?, ?, ?, ?, ?)
                """,
                (eval_id, crit_id, rating, score, ""),
            )

        # سجل التاريخ (لو الجدول موجود)
        try:
            cur.execute(
                """
                INSERT INTO evaluation_history
                (evaluation_id, action, changed_by, notes)
                VALUES (?, 'created', ?, 'تم إنشاء تقييم وهمي')
                """,
                (eval_id, 1),
            )
        except sqlite3.OperationalError:
            # في حال عدم وجود جدول التاريخ
            pass


def create_fake_employees(n=250000):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # نحدد آخر id قبل الإضافة لنستخرج الموظفين الجدد فقط
    row = cur.execute("SELECT COALESCE(MAX(id), 0) FROM employees").fetchone()
    start_max_id = row[0] if row else 0

    departments = ["Human Resources", "IT", "Finance", "Sales", "Marketing", "Operations"]
    positions = [
        "Department Manager", "HR Specialist", "Accountant",
        "Software Developer", "Systems Analyst", "Sales Representative",
        "Technical Support", "Project Coordinator", "Financial Analyst",
    ]

    created = 0
    i = 1
    while created < n:
        first = random.choice(FIRST_NAMES)
        medium=random.choice(LAST_NAMES)
        last = random.choice(LAST_NAMES)
        base_name = f"{first} {medium} {last}"
        name = base_name

        # لو الاسم موجود بالفعل، جرّب تضيف رقم عشوائي في الآخر لغاية ما يظبط
        suffix_try = 0
        while True:
            department = random.choice(departments)
            position = random.choice(positions)
            salary = round(random.uniform(3000, 15000), 2)
            phone = f"010{random.randint(10000000, 99999999)}"
            email = f"{first}_{last}@gmail.com"

            gov = random.choice(EGYPT_GOVS)
            street_no = random.randint(1, 200)
            address = f"{street_no} Street, {gov}"

            try:
                cur.execute(
                    """
                    INSERT INTO employees (name, department, position, salary, phone, email, address)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (name, department, position, salary, phone, email, address),
                )
                created += 1
                i += 1
                break
            except sqlite3.IntegrityError:
                suffix_try += 1
                # غيّر الاسم بإضافة رقم لآخره لتفادي UNIQUE constraint على name
                name = f"{base_name} #{suffix_try}"
                continue

    # جلب الـ IDs للموظفين الذين أُضيفوا في هذه العملية فقط
    new_ids_rows = cur.execute(
        "SELECT id FROM employees WHERE id > ?", (start_max_id,)
    ).fetchall()
    new_employee_ids = [r[0] for r in new_ids_rows]

    # إنشاء حضور/انصراف وهمي وتقييمات وهمية للموظفين الجدد
    if new_employee_ids:
        generate_fake_attendance(cur, new_employee_ids, days=30)
        generate_fake_evaluations(cur, new_employee_ids)

    conn.commit()
    conn.close()
    print(f"Inserted {created} employees with Egyptian addresses, attendance, and evaluations.")


if __name__ == "__main__":
    create_fake_employees(250000)