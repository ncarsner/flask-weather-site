cities = {
    "Africa": [
        "Abidjan", "Addis Ababa", "Cairo", "Casablanca", "Dar es Salaam", "Johannesburg", "Kinshasa", 
        "Lagos", "Luanda", "Nairobi", "Accra", "Algiers", "Antananarivo", "Bamako", "Cape Town", 
        "Dakar", "Douala", "Durban", "Ibadan", "Kano", "Khartoum", "Kigali", "Lusaka", "Maputo", 
        "Monrovia", "Niamey", "Ouagadougou", "Port Harcourt", "Pretoria", "Yaounde"
    ],
    "Asia": [
        "Ahmedabad", "Alexandria", "Ankara", "Baghdad", "Bangalore", "Bangkok", "Beijing", "Chengdu", 
        "Chennai", "Chittagong", "Chongqing", "Delhi", "Dhaka", "Dongguan", "Foshan", "Guangzhou", 
        "Hangzhou", "Harbin", "Ho Chi Minh City", "Hong Kong", "Hyderabad", "Istanbul", "Jakarta", 
        "Jinan", "Kabul", "Karachi", "Kolkata", "Kuala Lumpur", "Lahore", "Manila", "Mumbai", 
        "Nanjing", "Osaka", "Pune", "Qingdao", "Riyadh", "Seoul", "Shanghai", "Shenzhen", "Singapore", 
        "Surat", "Suzhou", "Taipei", "Tehran", "Tianjin", "Tokyo", "Wuhan", "Xi'an", "Yangon", 
        "Zhengzhou", "Almaty", "Amman", "Baku", "Bandung", "Bishkek", "Colombo", "Damascus", 
        "Davao City", "Faisalabad", "Fukuoka", "Fuzhou", "Hanoi", "Hefei", "Hohhot", "Incheon", 
        "Islamabad", "Izmir", "Jaipur", "Jeddah", "Kathmandu", "Kuwait City", "Kyiv", "Lanzhou", 
        "Mashhad", "Medan", "Nagoya", "Nanchang", "Nanning", "Naypyidaw", "Palembang", "Patna", 
        "Phnom Penh", "Quito", "Recife", "Riverside", "Salvador", "San Antonio", "San Diego", 
        "San Francisco", "San Jose", "Santa Cruz", "Sapporo", "Semarang", "Sendai", "Shantou", 
        "Shenyang", "Shijiazhuang", "Tabriz", "Taiyuan", "Tangshan", "Tashkent", "Thessaloniki", 
        "Tijuana", "Tirana", "Tunis", "Ulaanbaatar", "Urumqi", "Valencia", "Vancouver", "Vienna", 
        "Warsaw", "Winnipeg", "Yaounde", "Yekaterinburg", "Yerevan", "Zibo", "Zurich"
    ],
    "Europe": [
        "Barcelona", "London", "Madrid", "Moscow", "Paris", "Saint Petersburg", "Athens", "Brussels", 
        "Bucharest", "Budapest", "Copenhagen", "Dresden", "Edinburgh", "Frankfurt", "Geneva", 
        "Gothenburg", "Hamburg", "Helsinki", "Krakow", "Lisbon", "Ljubljana", "Luxembourg", "Malaga", 
        "Marseille", "Milan", "Monaco", "Munich", "Naples", "Nice", "Oslo", "Prague", "Reykjavik", 
        "Riga", "Sarajevo", "Skopje", "Sofia", "Stuttgart", "Tallinn", "Tbilisi", "Thimphu", 
        "Torshavn", "Valletta", "Vilnius", "Warsaw", "Wellington", "Zagreb", "Zurich"
    ],
    "North America": [
        "Chicago", "Guadalajara", "Los Angeles", "Mexico City", "New York", "Toronto", "Albuquerque", 
        "Arlington", "Atlanta", "Austin", "Baltimore", "Boston", "Charlotte", "Cincinnati", 
        "Cleveland", "Colorado Springs", "Columbus", "Dallas", "Denver", "Detroit", "El Paso", 
        "Fort Worth", "Fresno", "Houston", "Indianapolis", "Jacksonville", "Kansas City", "Las Vegas", 
        "Long Beach", "Louisville", "Memphis", "Mesa", "Miami", "Milwaukee", "Minneapolis", 
        "Nashville", "New Orleans", "Oakland", "Oklahoma City", "Omaha", "Philadelphia", "Phoenix", 
        "Pittsburgh", "Portland", "Raleigh", "Sacramento", "San Antonio", "San Diego", "San Francisco", 
        "San Jose", "Seattle", "Tucson", "Tulsa", "Virginia Beach", "Washington", "Wichita", 
        "Anchorage", "Bakersfield", "Chandler", "Chesapeake", "Corpus Christi", "Durham", "Garland", 
        "Glendale", "Greensboro", "Henderson", "Hialeah", "Honolulu", "Irvine", "Irving", "Laredo", 
        "Lubbock", "Madison", "Norfolk", "Orlando", "Plano", "Reno", "Scottsdale", "Shreveport", 
        "Spokane", "St. Louis", "St. Paul", "St. Petersburg", "Stockton", "Tampa", "Toledo", 
        "Winston-Salem"
    ],
    "South America": [
        "Bogota", "Buenos Aires", "Lima", "Rio de Janeiro", "Santiago", "Sao Paulo", "Asuncion", 
        "Brasilia", "Caracas", "Cali", "Curitiba", "Guayaquil", "Managua", "Montevideo", "Panama City", 
        "Port Louis", "Port Moresby", "San Salvador", "Santa Cruz"
    ],
    "Oceania": [
        "Sydney", "Auckland", "Brisbane", "Melbourne", "Perth", "Adelaide", "Wellington", "Pohnpei",
    ],
    "Middle East": [
        "Abu Dhabi", "Doha", "Dubai", "Muscat", "Riyadh", "Manama", "Kuwait City", "Amman", "Beirut", 
        "Damascus", "Jerusalem", "Gaza", "Ramallah", "Nicosia", "Sanaa", "Baghdad", "Basra", "Erbil", 
        "Mosul", "Kirkuk", "Najaf", "Karbala", "Sulaymaniyah", "Tikrit", "Fallujah", "Samawah", 
        "Nasiriyah", "Diwaniyah", "Kut", "Amara", "Al Hillah", "Baqubah", "Balad", "Samarra", "Kufa",
    ]
}

world_cities = [city for continent in cities.values() for city in continent]
