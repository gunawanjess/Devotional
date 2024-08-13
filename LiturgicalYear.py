from datetime import date, datetime, timedelta
import random

class LiturgicalYear: # adapted from https://code.activestate.com/recipes/576518-liturgical-calendar-year-class/ with reduced liturgical seasons
    def __init__(self, year):
        self.init_calendar(year)

    def calc_easter(self, year):
        a = year % 19
        b = year // 100
        c = year % 100
        d = (19 * a + b - b // 4 - ((b - (b + 8) // 25 + 1) // 3) + 15) % 30
        e = (32 + 2 * (b % 4) + 2 * (c // 4) - d - (c % 4)) % 7
        f = d + e - 7 * ((a + 11 * d + 22 * e) // 451) + 114
        month = f // 31
        day = f % 31 + 1    
        return date(year, month, day)
    
    def init_calendar(self, year):
        self.easter = self.calc_easter(year + 1)
        
        nov27day = date(year, 11, 27).isoweekday()
        if nov27day == 7:
            self.advent1 = date(year, 11, 27)
        else:
            self.advent1 = date(year, 11, 27) + timedelta(7 - nov27day)
            
        self.advent4 = self.advent1 + timedelta(21)
        
        nov27day = date(year + 1, 11, 27).isoweekday()
        if nov27day == 7:
            next_advent1 = date(year + 1, 11, 27)
        else:
            next_advent1 = date(year + 1, 11, 27) + timedelta(7 - nov27day)
        
        jan6day = date(year + 1, 1, 6).isoweekday()
        if jan6day == 7:
            self.epiphany1 = date(year + 1, 1, 13)
        else:
            self.epiphany1 = date(year + 1, 1, 13) - timedelta(jan6day)
        
        self.epiphany = date(year + 1, 1, 6)
        self.ashWednesday = self.easter - timedelta(46)
        self.ascension = self.easter + timedelta(39)
        self.pentecost = self.easter + timedelta(49)
        self.trinity = self.easter + timedelta(56)
        
        self.epiphanySundays = (self.ashWednesday - self.epiphany1).days // 7 + 1
        self.trinitySundays = (next_advent1 - self.trinity).days // 7 - 1
        self.pentecostSundays = self.trinitySundays + 1

class LiturgicalPeriod:
    def __init__(self):
        today = date.today()
        current_year = today.year
        self.year = LiturgicalYear(current_year - 1 if today < date(current_year, 12, 1) else current_year)
        self.hymn_ranges = {
            "Advent": range(15, 19),
            "Christmas": range(19, 23),
            "Epiphany": range(23, 25),
            "Lent": range(25, 31),
            "Easter": range(31, 37),
            "Ascension": range(37, 47),
            "Pentecost": range(47, 51),
            "Trinity": list(range(3, 15)) + list(range(51, 86))
        }

    def get_current_period(self):
        today = date.today()
        if today < self.year.advent1:
            return "Trinity"
        elif today <= self.year.advent4:
            return "Advent"
        elif today < self.year.epiphany:
            return "Christmas"
        elif today < self.year.ashWednesday:
            return "Epiphany"
        elif today < self.year.easter:
            return "Lent"
        elif today < self.year.ascension:
            return "Easter"
        elif today < self.year.pentecost:
            return "Ascension"
        elif today < self.year.trinity:
            return "Pentecost"
        else:
            return "Trinity"

    def get_random_hymn(self):
        period = self.get_current_period()
        hymn_range = self.hymn_ranges[period]
        return random.choice(hymn_range)

    def get_prayer_time(self):
        current_hour = datetime.now().hour
        if current_hour < 12:
            return "Morning Prayer"
        else:
            return "Evening Prayer"
        
    def get_prayer_text(self): # adapted from the 2014 Book of Praise
        current_hour = datetime.now().hour
        if current_hour < 12:
            return "Merciful Father, we thank you that in your great faithfulness you kept watch over us during this past night. Strengthen and guide us by your Holy Spirit, that we may use this new day and all the days of our life in holiness and righteousness. Grant that we in all our undertakings may always have your glory foremost in our minds. May we always work in such a manner that we expect all results and fruits of our work from your generous hand alone. We ask that you will graciously forgive all our sins according to your promise, for the sake of the passion and blood of our Lord Jesus Christ. Through your grace we are heartily sorry for all our transgressions. Illumine our hearts, that we may lay aside all works of darkness and as children of light may walk in the light and live a new life in all godliness. Bless the proclamation of your divine Word here and in the mission fields. Strengthen all faithful labourers in your vineyard. We pray for those whom you have set over us, that as servants of you, the King of kings and Lord of lords, they may rule according to the calling you give them. Give endurance to all who are persecuted because of their faith and deliver them from their enemies. Destroy all the works of the devil. Comfort the distressed. Show your mercy and help to all who call upon your holy name in sickness and other trials of life. Deal with us and with all your people according to your grace in Christ Jesus our Lord, who assured us that you will do whatever we ask in his name. Amen."
        else:
            return "Merciful God, in whom is no darkness at all, we come before you at the end of this day. We thank you that you have given us strength for our daily work, and have guided us safely through this day. Bless what was good in our labour and conduct. Since you ordained that man should labour during the day and rest at night, we pray you to give us peaceful and undisturbed rest so that we may be able to take up our daily task again. Command your angels to guard us and cause your face to shine upon us. We cast all our anxieties on you, for you take care of us. Control our sleep and rule our hearts, in order that we may not be defiled in any way but may glorify you even in our nightly rest. Defend and protect us against all assaults of the devil and take us into your divine protection. We confess that we did not spend this day without grievously sinning against you. In your mercy please cover our sins as you cover the earth in the darkness of the night. Grant comfort and rest to all who are ill, bowed down with grief, or afflicted with spiritual distress. Your steadfast love, O Lord, endures forever. Do not abandon the works of your hands. All this we ask in the name of Jesus Christ our Lord. Amen."    

    def get_random_confession(self):
        return random.choice(["Psalm 32", "Psalm 51"])
    
    def get_random_psalm(self):
        return random.randint(1, 150)

    def get_random_credo(self):
        return random.choice(["recited", "Hymn 1", "Hymn 2"])
    
    def get_bible_reading(self):   
        # Extract the year and the day of the year
        today = date.today()    
        current_year = today.year
        day_number = today.timetuple().tm_yday
        
        bible_reading_plan = [ # adapted from https://uploads.crossway.org/excerpt/story-of-redemption-bible-reading-plan.pdf with modification to accommodate for 366 days
        "Genesis 1-3", "Genesis 4-7", "Genesis 8-11", "Genesis 12-15", "Genesis 16-18", 
        "Genesis 19-21", "Genesis 22-24", "Genesis 25-26", "Genesis 27-29", "Genesis 30-31",
        "Genesis 32-34", "Genesis 35-37", "Genesis 38-40", "Genesis 41-42", "Genesis 43-45", 
        "Genesis 46-47", "Genesis 48-50", "Exodus 1-3", "Exodus 4-6", "Exodus 7-9", 
        "Exodus 10-12", "Exodus 13-15", "Exodus 16-18", "Exodus 19-21", "Exodus 22-24", 
        "Exodus 25-27", "Exodus 28-29", "Exodus 30-32", "Exodus 33-35", "Exodus 36-38", 
        "Exodus 39-40", "Leviticus 1-4", "Leviticus 5-7", "Leviticus 8-10", "Leviticus 11-13", 
        "Leviticus 14-15", "Leviticus 16-18", "Leviticus 19-21", "Leviticus 22-23", 
        "Leviticus 24-25", "Leviticus 26-27", "Numbers 1-2", "Numbers 3-4", "Numbers 5-6", 
        "Numbers 7-8", "Numbers 9-10", "Numbers 11-13", "Numbers 14-15", "Numbers 16-17", 
        "Numbers 18-20", "Numbers 21-22", "Numbers 23-25", "Numbers 26-27", "Numbers 28-30", 
        "Numbers 31-32", "Numbers 33-34", "Numbers 35-36", "Deuteronomy 1-2", "Deuteronomy 3-4", 
        "Deuteronomy 5-7", "Deuteronomy 8-10", "Deuteronomy 11-13", "Deuteronomy 14-16", 
        "Deuteronomy 17-20", "Deuteronomy 21-23", "Deuteronomy 24-27", "Deuteronomy 28-29", 
        "Deuteronomy 30-31", "Deuteronomy 32-34", "Joshua 1-4", "Joshua 5-8", "Joshua 9-11", 
        "Joshua 12-15", "Joshua 16-18", "Joshua 19-21", "Joshua 22-24", "Judges 1-2", 
        "Judges 3-5", "Judges 6-7", "Judges 8-9", "Judges 10-12", "Judges 13-15", 
        "Judges 16-18", "Judges 19-21", "Ruth", "1 Samuel 1-3", "1 Samuel 4-8", 
        "1 Samuel 9-12", "1 Samuel 13-14", "1 Samuel 15-17", "1 Samuel 18-20",
        "1 Samuel 21-24", "1 Samuel 25-27", "1 Samuel 28-31", "2 Samuel 1-3",
        "2 Samuel 4-7", "2 Samuel 8-11", "2 Samuel 12-15", "2 Samuel 16-18",
        "2 Samuel 19-21", "2 Samuel 22-24", "1 Kings 1-2", "1 Kings 3-4",
        "Proverbs 1-4", "Proverbs 5-9", "Proverbs 10-11", "Proverbs 12-13",
        "Proverbs 14-15", "Proverbs 16-18", "Proverbs 19-21", "Proverbs 22-23",
        "Proverbs 24-26", "Proverbs 27-29", "Proverbs 30-31", "Ecclesiastes 1-4",
        "Ecclesiastes 5-8", "Ecclesiastes 9-12", "Job 1-3", "Job 4-7", "Job 8-10",
        "Job 11-13", "Job 14-16", "Job 17-20", "Job 21-23", "Job 24-28", "Job 29-31",
        "Job 32-34", "Job 35-37", "Job 38-39", "Job 40-42", "Song of Solomon",
        "1 Kings 5-7", "1 Kings 8-9", "1 Kings 10-11", "1 Kings 12-14",
        "1 Kings 15-17", "1 Kings 18-20", "1 Kings 21-22", "2 Kings 1-3",
        "2 Kings 4-5", "2 Kings 6-8", "2 Kings 9-11", "2 Kings 12-14",
        "2 Kings 15:1-17:13", "Amos 1-5", "Amos 6-9", "Hosea 1-7", "Hosea 8-14",
        "Micah", "2 Kings 17:14-33; Jonah", "2 Kings 17:34-19:37", "Nahum",
        "2 Kings 20:1-22:2", "Zephaniah", "Joel", "2 Kings 22:3-24:20",
        "Habakkuk; Obadiah; 2 Kings 25", "Isaiah 1-4", "Isaiah 5-8", "Isaiah 9-12",
        "Isaiah 13-17", "Isaiah 18-22", "Isaiah 23-27", "Isaiah 28-30", "Isaiah 31-35",
        "Isaiah 36-39", "Isaiah 40-43", "Isaiah 44-48", "Isaiah 49-53", "Isaiah 54-58",
        "Isaiah 59-62", "Isaiah 63-66", "Jeremiah 1-3", "Jeremiah 4-6", "Jeremiah 7-9",
        "Jeremiah 10-13", "Jeremiah 14-17", "Jeremiah 18-22", "Jeremiah 23-25", "Jeremiah 26-29",
        "Jeremiah 30-31", "Jeremiah 32-34", "Jeremiah 35-37", "Jeremiah 38-41", "Jeremiah 42-45",
        "Jeremiah 46-48", "Jeremiah 49-50", "Jeremiah 51-52", "Lamentations 1-2", "Lamentations 3-5",
        "Ezekiel 1-4", "Ezekiel 5-8", "Ezekiel 9-12", "Ezekiel 13-15", "Ezekiel 16-17", "Ezekiel 18-20",
        "Ezekiel 21-22", "Ezekiel 23-24", "Ezekiel 25-27", "Ezekiel 28-30", "Ezekiel 31-33", "Ezekiel 34-36",
        "Ezekiel 37-39", "Ezekiel 40-42", "Ezekiel 43-45", "Ezekiel 46-48", "Daniel 1-3", "Daniel 4-6",
        "Daniel 7-9", "Daniel 10-12", "1 Chronicles 1-2", "1 Chronicles 3-4", "1 Chronicles 5-6",
        "1 Chronicles 7-8", "1 Chronicles 9-11", "1 Chronicles 12-14", "1 Chronicles 15-17",
        "1 Chronicles 18-21", "1 Chronicles 22-24", "1 Chronicles 25-27", "1 Chronicles 28-29",
        "2 Chronicles 1-4", "2 Chronicles 5-8", "2 Chronicles 9-12", "2 Chronicles 13-16",
        "2 Chronicles 17-20", "2 Chronicles 21-24", "2 Chronicles 25-27", "2 Chronicles 28-31",
        "2 Chronicles 32-34", "2 Chronicles 35-36", "Ezra 1:1-5:1", "Haggai; Zechariah 1-6",
        "Zechariah 7-14", "Ezra 5:2-6:22; Esther 1-2", "Esther 3-5", "Esther 6-10", "Ezra 7-10",
        "Nehemiah 1-3", "Nehemiah 4-5", "Nehemiah 6-7", "Nehemiah 8-9", "Nehemiah 10-11",
        "Nehemiah 12-13", "Psalms 1-8", "Psalms 9-16", "Psalms 17-20", "Psalms 21-25",
        "Psalms 26-31", "Psalms 32-35", "Psalms 36-39", "Psalms 40-45", "Psalms 46-50",
        "Psalms 51-57", "Psalms 58-65", "Psalms 66-69", "Psalms 70-73", "Psalms 74-77",
        "Psalms 78-79", "Psalms 80-85", "Psalms 86-89", "Psalms 90-95", "Psalms 96-102",
        "Psalms 103-105", "Psalms 106-107", "Psalms 108-114", "Psalms 115-118", "Psalms 119:1-88",
        "Psalms 119:89-176", "Psalms 120-132", "Psalms 133-139", "Psalms 140-145", "Psalms 146-150",
        "Malachi", "Matthew 1-2", "Matthew 3-4", "Matthew 5-7", "Matthew 8-10", "Matthew 11-12",
        "Matthew 13-14", "Matthew 15-17", "Matthew 18-19", "Matthew 20-21", "Matthew 22-23",
        "Matthew 24-25", "Matthew 26", "Matthew 27-28", "Mark 1-3", "Mark 4-5", "Mark 6-7",
        "Mark 8-9", "Mark 10-11", "Mark 12-13", "Mark 14", "Mark 15-16", "John 1-2", "John 3-4",
        "John 5-6", "John 7-8", "John 9-10", "John 11-13", "John 14-16", "John 17-19", "John 20-21",
        "Luke 1", "Luke 2-3", "Luke 4-5", "Luke 6-7", "Luke 8-9", "Luke 10-11", "Luke 12-13",
        "Luke 14-15", "Luke 16-17", "Luke 18-19", "Luke 20-21", "Luke 22", "Luke 23-24", "Acts 1-3",
        "Acts 4-6", "Acts 7-8", "Acts 9-10", "Acts 11-13", "Acts 14-15", "Acts 16-18", "Acts 19-20",
        "Acts 21-23", "Acts 24-26", "Acts 27-28", "1 Thessalonians 1-5", "2 Thessalonians",
        "Galatians 1-6", "1 Corinthians 1-4", "1 Corinthians 5-7", "1 Corinthians 8-11",
        "1 Corinthians 12-14", "1 Corinthians 15-16", "2 Corinthians 1-4", "2 Corinthians 5-9",
        "2 Corinthians 10-13", "Romans 1-2", "Romans 3-4", "Romans 5-7", "Romans 8-10",
        "Romans 11-13", "Romans 14-16", "Colossians; Philemon", "Ephesians 1-3", "Ephesians 4-6",
        "Philippians 1-4", "1 Timothy 1-3", "1 Timothy 4-6", "Titus", "1 Peter 1-2", "1 Peter 3-5",
        "Hebrews 1-2", "Hebrews 3-5", "Hebrews 6-8", "Hebrews 9-10", "Hebrews 11-13", "2 Timothy 1-4",
        "2 Peter", "Jude", "James 1-3", "James 4-5", "1 John 1-3", "1 John 4-5", "2-3 John",
        "Revelation 1-3", "Revelation 4-7", "Revelation 8-11", "Revelation 12-15", "Revelation 16-18",
        "Revelation 19-20", "Revelation 21-22"
    ]
        return bible_reading_plan[day_number - 1]  # Subtract 1 because list indices start at 0

    def run_random_hymn(self):
        prayer_time = self.get_prayer_time()
        prayer_text = self.get_prayer_text()
        confession_number = self.get_random_confession()
        bible_reading = self.get_bible_reading()
        credo_number = self.get_random_credo()
        hymn_number = self.get_random_hymn()
        psalm_number = self.get_random_psalm()
        today = date.today()

        print(f"{prayer_time}")
        print(today)
        print("Our help is in the name of the Lord, who made heaven and earth. \nGrace to you and peace from God our Father and the Lord Jesus Christ.")
        print(f"{prayer_text}")
        print("You shall love the Lord your God with all your heart and with all your soul and with all your mind... You shall love your neighbor as yourself. On these two commandments depend all the Law and the Prophets.")
        print(f"Confession: {confession_number}")
        print("If we confess our sins, he is faithful and just to forgive us our sins and to cleanse us from all unrighteousness.")
        print(f"Bible reading: {bible_reading}")
        print(f"Psalm: Psalm {psalm_number}")
        print(f"Hymn for {self.get_current_period()}: Hymn {hymn_number}")
        print(f"Credo: {credo_number}")
        print("The grace of the Lord Jesus Christ and the love of God and the fellowship of the Holy Spirit be with you all.")
        print("Program by Jess Gunawan for personal use only. All Scriptural quotations are taken from the English Standard Version. Hymn numbers and prayers are taken from the Book of Praise of the Canadian Reformed churches.")

# Example usage:
period_finder = LiturgicalPeriod()
period_finder.run_random_hymn()
