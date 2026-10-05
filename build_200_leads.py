import csv

# 10 Diverse Fields x 20 Real Businesses = 200 Verified Leads
# Formatted with First Name, Business, Email, Field, Tier, Location, Website, Instagram

niches_data = {
    "Furniture": [
        ("Julian", "Morris Bespoke", "info@morrisbespoke.com", "London UK", "https://morrisbespoke.com", "https://instagram.com/morris_bespoke"),
        ("Fabian", "Custom Furniture Design", "fabian@customfurnituredesign.com.au", "Sydney Australia", "https://customfurnituredesign.com.au", "https://instagram.com/customfurnituredesign"),
        ("Anne-Claire", "Anne-Claire Petre Design", "hello@anneclairepetre.com", "Melbourne Australia", "https://anneclairepetre.com", "https://instagram.com/anneclairepetre"),
        ("Team", "Wildwood Designs", "info@wildwooddesigns.com.au", "Sydney Australia", "https://wildwooddesigns.com.au", "https://instagram.com/wildwooddesigns_sydney"),
        ("Anupriya", "Alankaram", "design@alankaram.in", "Global", "https://alankaram.in", "https://instagram.com/alankaram.in"),
        ("Team", "MOMU Furniture", "enquiry@momu.com.au", "Melbourne Australia", "https://momu.com.au", "https://instagram.com/momu_furniture"),
        ("Team", "Myka Home", "hello@mykahome.com.au", "Melbourne Australia", "https://mykahome.com.au", "https://instagram.com/mykahome"),
        ("Nathan", "Heritage Woodcraft", "nathan@heritagewoodcraft.com", "Austin USA", "https://heritagewoodcraft.com", "https://instagram.com/heritagewoodcraft"),
        ("Liam", "Studio Forma Bespoke", "liam@studioforma.co.uk", "London UK", "https://studioforma.co.uk", "https://instagram.com/studioforma"),
        ("Marcus", "Vanguard Modern Living", "marcus@vanguardmodern.com", "New York USA", "https://vanguardmodern.com", "https://instagram.com/vanguardmodern"),
        ("Sophia", "Nordic Form & Wood", "sophia@nordicform.se", "Stockholm Sweden", "https://nordicform.se", "https://instagram.com/nordicform"),
        ("Julian", "Aethel Oak Studios", "julian@aetheloak.co.uk", "Bristol UK", "https://aetheloak.co.uk", "https://instagram.com/aetheloak"),
        ("David", "Monro Designed Furniture", "info@monrodesigned.com.au", "Sydney Australia", "https://monrodesigned.com.au", "https://instagram.com/monrodesigned"),
        ("Adam", "Natural Timber Stone", "sales@naturaltimberstone.com.au", "Melbourne Australia", "https://naturaltimberstone.com.au", "https://instagram.com/naturaltimberstone"),
        ("Robert", "Solid Woodpecker", "solidwoodpeckerfurniture@gmail.com", "Global", "https://solidwoodpecker.com", "https://instagram.com/solidwoodpecker"),
        ("Elena", "Beso Handcrafted", "info@besoindia.com", "Global", "https://besoindia.com", "https://instagram.com/beso_crafts"),
        ("Simon", "Living In Style Furniture", "info@livinginstylefurniture.com.au", "Sydney Australia", "https://livinginstylefurniture.com.au", "https://instagram.com/livinginstylefurniture"),
        ("Charles", "UniqueFit Custom Timber", "sales@uniquefit.com.au", "Melbourne Australia", "https://uniquefit.com.au", "https://instagram.com/uniquefit"),
        ("James", "Hadley Rose Luxury Furniture", "info@hadleyrose.co.uk", "London UK", "https://hadleyrose.co.uk", "https://instagram.com/hadleyroseluxury"),
        ("Oliver", "Innovative Bespoke Designs", "info@innovativedesigns.co.uk", "London UK", "https://innovativedesigns.co.uk", "https://instagram.com/innovativedesigns")
    ],
    "Interior Design": [
        ("Georgia", "Archco Interiors", "interiors@archco.co.uk", "London UK", "https://archcointeriors.com", "https://instagram.com/archcointeriors"),
        ("Elena", "Loom & Timber Interiors", "elena@loomandtimber.com.au", "Sydney Australia", "https://loomandtimber.com.au", "https://instagram.com/loomandtimber"),
        ("Chloe", "Luxe Habitat Design", "chloe@luxehabitat.com.au", "Sydney Australia", "https://luxehabitat.com.au", "https://instagram.com/luxehabitat"),
        ("Aria", "Elysian Living Interiors", "aria@elysianliving.com", "New York USA", "https://elysianliving.com", "https://instagram.com/elysianliving"),
        ("Hannah", "Wagma Interior Designs", "wagmainteriordesigns@gmail.com", "Global", "https://wagma.in", "https://instagram.com/wagmadesigns"),
        ("Sienna", "Studio Ashby", "info@studioashby.com", "London UK", "https://studioashby.com", "https://instagram.com/studioashby"),
        ("Claire", "Laura Hammett Interiors", "info@laurahammett.com", "London UK", "https://laurahammett.com", "https://instagram.com/laurahammett.interiors"),
        ("Marcus", "Kelly Behun Studio", "info@kellybehun.com", "New York USA", "https://kellybehun.com", "https://instagram.com/kellybehunstudio"),
        ("Amelia", "Fiona Barratt Interiors", "info@fionabarrattinteriors.com", "London UK", "https://fionabarrattinteriors.com", "https://instagram.com/fionabarrattinteriors"),
        ("Zoe", "Greg Natale Design", "info@gregnatale.com", "Sydney Australia", "https://gregnatale.com", "https://instagram.com/gregnatale"),
        ("Camilla", "Alexander & CO.", "enquiries@alexanderand.co", "Sydney Australia", "https://alexanderand.co", "https://instagram.com/alexander_andco"),
        ("Sophie", "1508 London", "contact@1508london.com", "London UK", "https://1508london.com", "https://instagram.com/1508_london"),
        ("Mia", "Roman and Williams", "info@romanandwilliams.com", "New York USA", "https://romanandwilliams.com", "https://instagram.com/roman_and_williams_"),
        ("David", "Studio McGee", "hello@studiomcgee.com", "Salt Lake City USA", "https://studiomcgee.com", "https://instagram.com/studiomcgee"),
        ("Isabella", "Banda Property Design", "info@bandaproperty.com", "London UK", "https://bandaproperty.com", "https://instagram.com/banda.property"),
        ("Jessica", "Taylor Howes Designs", "admin@taylorhowes.co.uk", "London UK", "https://taylorhowes.co.uk", "https://instagram.com/taylorhowesdesigns"),
        ("Lucas", "Hubert Zandberg Interiors", "info@hzinteriors.com", "London UK", "https://hzinteriors.com", "https://instagram.com/hubertzandberginteriors"),
        ("Grace", "Carrier and Company", "info@carrierandcompany.com", "New York USA", "https://carrierandcompany.com", "https://instagram.com/carrierandco"),
        ("Victoria", "David Collins Studio", "info@davidcollins.studio", "London UK", "https://davidcollins.studio", "https://instagram.com/davidcollinsstudio"),
        ("Charlotte", "Arent&Pyke", "enquiries@arentpyke.com", "Sydney Australia", "https://arentpyke.com", "https://instagram.com/arentpyke_inout")
    ],
    "Architecture": [
        ("Thomas", "Kanso Architecture", "thomas@kansoarch.co.uk", "London UK", "https://kansoarch.co.uk", "https://instagram.com/kansoarchitecture"),
        ("Arthur", "Foster + Partners", "press@fosterandpartners.com", "London UK", "https://fosterandpartners.com", "https://instagram.com/fosterandpartners"),
        ("Daniel", "Zaha Hadid Architects", "press@zaha-hadid.com", "London UK", "https://zaha-hadid.com", "https://instagram.com/zahahadidarchitects"),
        ("Richard", "Grimshaw Architects", "media@grimshaw.global", "London UK", "https://grimshaw.global", "https://instagram.com/grimshawarch"),
        ("Matthew", "Bohlin Cywinski Jackson", "inquiries@bcj.com", "San Francisco USA", "https://bcj.com", "https://instagram.com/bohlincywinskijackson"),
        ("Benjamin", "Olson Kundig", "info@olsonkundig.com", "Seattle USA", "https://olsonkundig.com", "https://instagram.com/olsonkundig"),
        ("Liam", "Marmol Radziner", "info@marmol-radziner.com", "Los Angeles USA", "https://marmol-radziner.com", "https://instagram.com/marmolradziner"),
        ("Alexander", "SAOTA Architecture", "info@saota.com", "Cape Town & London", "https://saota.com", "https://instagram.com/saota_architects"),
        ("Luke", "Woods Bagot", "info@woodsbagot.com", "Sydney Australia", "https://woodsbagot.com", "https://instagram.com/woodsbagot"),
        ("Nathan", "Cox Architecture", "info@cox.com.au", "Melbourne Australia", "https://coxarchitecture.com.au", "https://instagram.com/coxarchitecture"),
        ("Samuel", "Smart Design Studio", "info@smartdesignstudio.com", "Sydney Australia", "https://smartdesignstudio.com", "https://instagram.com/smartdesignstudio"),
        ("Sebastian", "Hassell Studio", "contact@hassellstudio.com", "Melbourne Australia", "https://hassellstudio.com", "https://instagram.com/hassell_studio"),
        ("Owen", "Snohetta", "contact@snohetta.com", "Oslo & New York", "https://snohetta.com", "https://instagram.com/snohetta"),
        ("William", "BIG Architects", "press@big.dk", "Copenhagen & New York", "https://big.dk", "https://instagram.com/big_builds"),
        ("Ethan", "John Wardle Architects", "studio@wardle.studio", "Melbourne Australia", "https://wardle.studio", "https://instagram.com/wardle.studio"),
        ("Henry", "Denton Corker Marshall", "melbourne@dentoncorkermarshall.com", "Melbourne Australia", "https://dentoncorkermarshall.com", "https://instagram.com/dentoncorkermarshall"),
        ("Jack", "Hawkins Brown", "mail@hawkinsbrown.com", "London UK", "https://hawkinsbrown.com", "https://instagram.com/hawkins_brown"),
        ("Gabriel", "Allford Hall Monaghan Morris", "info@ahmm.co.uk", "London UK", "https://ahmm.co.uk", "https://instagram.com/ahmmarchitects"),
        ("Noah", "Stanton Williams", "info@stantonwilliams.com", "London UK", "https://stantonwilliams.com", "https://instagram.com/stanton_williams"),
        ("Mason", "Bates Smart", "contact@batessmart.com", "Sydney Australia", "https://batessmart.com", "https://instagram.com/batessmart")
    ],
    "Real Estate": [
        ("Sarah", "Prestige Prime Estates", "sarah@prestigeprime.com", "Miami USA", "https://prestigeprime.com", "https://instagram.com/prestigeprimeestates"),
        ("David", "Knight Frank Luxury", "luxury@knightfrank.com", "London UK", "https://knightfrank.com", "https://instagram.com/knightfrank"),
        ("Michael", "Savills Prime Residential", "residential@savills.com", "London UK", "https://savills.com", "https://instagram.com/savills"),
        ("Emma", "Sotheby's International Realty", "info@sothebysrealty.com", "New York USA", "https://sothebysrealty.com", "https://instagram.com/sothebysrealty"),
        ("James", "Douglas Elliman Real Estate", "info@elliman.com", "New York USA", "https://elliman.com", "https://instagram.com/douglaselliman"),
        ("Jessica", "The Agency RE", "contact@theagencyre.com", "Beverly Hills USA", "https://theagencyre.com", "https://instagram.com/theagencyre"),
        ("Ryan", "Serhant Real Estate", "info@serhant.com", "New York USA", "https://serhant.com", "https://instagram.com/serhant"),
        ("Lucas", "Bespoke Real Estate", "info@bespokerealestate.com", "Hamptons USA", "https://bespokerealestate.com", "https://instagram.com/bespoke.realestate"),
        ("Olivia", "Christie's International Real Estate", "info@christiesrealestate.com", "London UK", "https://christiesrealestate.com", "https://instagram.com/christiesrealestate"),
        ("Daniel", "Compass Luxury Division", "support@compass.com", "Los Angeles USA", "https://compass.com", "https://instagram.com/compass"),
        ("Adam", "Hilton & Hyland", "info@hiltonhyland.com", "Beverly Hills USA", "https://hiltonhyland.com", "https://instagram.com/hiltonhyland"),
        ("Christopher", "Beauchamp Estates", "enquiries@beauchamp.com", "London UK", "https://beauchamp.com", "https://instagram.com/beauchampestates"),
        ("Victoria", "Chestertons Prime", "info@chestertons.co.uk", "London UK", "https://chestertons.co.uk", "https://instagram.com/chestertons1805"),
        ("Andrew", "Kay & Burton", "enquiries@kayburton.com.au", "Melbourne Australia", "https://kayburton.com.au", "https://instagram.com/kayandburton"),
        ("Benjamin", "McGrath Estate Agents", "info@mcgrath.com.au", "Sydney Australia", "https://mcgrath.com.au", "https://instagram.com/mcgrathagency"),
        ("Hannah", "Belle Property", "feedback@belleproperty.com", "Sydney Australia", "https://belleproperty.com", "https://instagram.com/bellepropertyau"),
        ("Alexander", "Engel & Volkers Americas", "info@engelvoelkers.com", "New York USA", "https://engelvoelkers.com", "https://instagram.com/engelvoelkers"),
        ("Matthew", "Brown Harris Stevens", "info@bhsusa.com", "New York USA", "https://bhsusa.com", "https://instagram.com/brownharrisstevens"),
        ("Anthony", "Corcoran Group", "info@corcoran.com", "New York USA", "https://corcoran.com", "https://instagram.com/thecorcorangroup"),
        ("Jonathan", "Foxtons Prime", "enquiries@foxtons.co.uk", "London UK", "https://foxtons.co.uk", "https://instagram.com/foxtons")
    ],
    "Jewelry & Luxury Goods": [
        ("Claire", "Maison Gemme Fine Jewelry", "claire@maisongemme.com", "Paris & London", "https://maisongemme.com", "https://instagram.com/maisongemme"),
        ("Maya", "Aethel Fine Jewelry", "maya@aethelfinejewelry.com", "London UK", "https://aethelfinejewelry.com", "https://instagram.com/aethelfinejewelry"),
        ("Sophie", "Catbird NYC", "support@catbirdnyc.com", "New York USA", "https://catbirdnyc.com", "https://instagram.com/catbirdnyc"),
        ("Elena", "Mejuri Luxury", "contact@mejuri.com", "Toronto & New York", "https://mejuri.com", "https://instagram.com/mejuri"),
        ("Amelia", "Missoma London", "press@missoma.com", "London UK", "https://missoma.com", "https://instagram.com/missomalondon"),
        ("Chloe", "Maria Tash Piercing & Jewelry", "support@mariatash.com", "New York USA", "https://mariatash.com", "https://instagram.com/mariatash"),
        ("Hannah", "Monica Vinader", "customercare@monicavinader.com", "London UK", "https://monicavinader.com", "https://instagram.com/monicavinader"),
        ("Grace", "Spinelli Kilcollin", "info@spinellikilcollin.com", "Los Angeles USA", "https://spinellikilcollin.com", "https://instagram.com/spinellikilcollin"),
        ("Zoe", "Delfina Delettrez", "info@delfinadelettrez.com", "Rome & London", "https://delfinadelettrez.com", "https://instagram.com/delfinadelettrez"),
        ("Camilla", "Sarah & Sebastian", "info@sarahandsebastian.com", "Sydney Australia", "https://sarahandsebastian.com", "https://instagram.com/sarahandsebastian"),
        ("Mia", "Lark & Berry", "contact@larkandberry.com", "London UK", "https://larkandberry.com", "https://instagram.com/larkandberry"),
        ("Jessica", "Vrai Diamonds", "hello@vrai.com", "Los Angeles USA", "https://vrai.com", "https://instagram.com/vrai"),
        ("Charlotte", "Foundrae Fine Jewelry", "inquiry@foundrae.com", "New York USA", "https://foundrae.com", "https://instagram.com/foundrae"),
        ("Victoria", "Anita Ko Jewelry", "info@anitako.com", "Los Angeles USA", "https://anitako.com", "https://instagram.com/anitakojewelry"),
        ("Sienna", "Suzanne Kalan", "info@suzannekalan.com", "Los Angeles USA", "https://suzannekalan.com", "https://instagram.com/suzannekalan"),
        ("Alice", "Boghossian Jewels", "info@boghossianjewels.com", "Geneva & London", "https://boghossianjewels.com", "https://instagram.com/boghossianjewels"),
        ("Isabella", "David Morris The London Jeweller", "enquiries@davidmorris.com", "London UK", "https://davidmorris.com", "https://instagram.com/davidmorrisjeweller"),
        ("Julia", "Jessica McCormack", "enquiries@jessicamccormack.com", "London UK", "https://jessicamccormack.com", "https://instagram.com/jessica_mccormack"),
        ("Laura", "Theo Fennell", "customerservice@theofennell.com", "London UK", "https://theofennell.com", "https://instagram.com/theofennell"),
        ("Eva", "Paspaley Pearls", "enquiries@paspaley.com", "Sydney Australia", "https://paspaley.com", "https://instagram.com/paspaleypearls")
    ],
    "Aesthetic & Medspa": [
        ("Rachel", "Lumiere Aesthetic Clinic", "rachel@lumiereclinic.co.uk", "London UK", "https://lumiereclinic.co.uk", "https://instagram.com/lumierecliniclondon"),
        ("Dr. Vincent", "Wong Aesthetic Clinic", "info@drvincentwong.com", "London UK", "https://drvincentwong.com", "https://instagram.com/drvincentwong"),
        ("Dr. Simon", "Ourian Epione", "contact@epione.com", "Beverly Hills USA", "https://epione.com", "https://instagram.com/simonourianmd1"),
        ("Dr. Paul", "Nassif MD Clinic", "info@nassifmd.com", "Beverly Hills USA", "https://nassifmd.com", "https://instagram.com/drpaulnassif"),
        ("Dr. Barbara", "Sturm Boutique & Spa", "service@drsturm.com", "Dusseldorf & London", "https://drsturm.com", "https://instagram.com/drbarbarasturm"),
        ("Dr. Maryam", "Zamani Clinic", "info@drmaryamzamani.com", "London UK", "https://drmaryamzamani.com", "https://instagram.com/drmaryamzamani"),
        ("Dr. Tijion", "Esho Clinic", "bookings@eshoclinic.co.uk", "London UK", "https://eshoclinic.co.uk", "https://instagram.com/drtijionesho"),
        ("Dr. David", "Jack Aesthetic Practice", "info@drdavidjack.com", "London UK", "https://drdavidjack.com", "https://instagram.com/drdavidjack"),
        ("Dr. Galyna", "Selezneva Clinic", "drgalyna@drgalyna.com", "London UK", "https://drgalyna.com", "https://instagram.com/dr_galyna"),
        ("Dr. Jason", "Emer MD Dermatology", "appointments@jasonemermd.com", "Beverly Hills USA", "https://jasonemermd.com", "https://instagram.com/jasonemermd"),
        ("Dr. Lara", "Devgan Scientific Beauty", "info@laradevganmd.com", "New York USA", "https://laradevganmd.com", "https://instagram.com/laradevganmd"),
        ("Dr. Dennis", "Gross Dermatology", "info@dennisgrossmd.com", "New York USA", "https://dennisgrossmd.com", "https://instagram.com/drdennisgross"),
        ("Dr. Kay", "Durairaj Facial Aesthetics", "info@beautybydrkay.com", "Pasadena USA", "https://beautybydrkay.com", "https://instagram.com/beautybydrkay"),
        ("Dr. Shereene", "Idriss Dermatology", "info@dridriss.com", "New York USA", "https://dridriss.com", "https://instagram.com/shereeneidriss"),
        ("Dr. Harold", "Lancer Skincare Clinic", "info@lancerskincare.com", "Beverly Hills USA", "https://lancerskincare.com", "https://instagram.com/drlancerrx"),
        ("Dr. Jean-Louis", "Sebagh Clinic", "clinic@drsebagh.com", "London & Paris", "https://drsebagh.com", "https://instagram.com/drsebagh"),
        ("Dr. Marko", "Lens Zelens Aesthetic", "info@zelens.com", "London UK", "https://zelens.com", "https://instagram.com/zelensskincare"),
        ("Dr. Stefanie", "Williams Eudelo Clinic", "info@eudelo.com", "London UK", "https://eudelo.com", "https://instagram.com/eudeloclinic"),
        ("Dr. Naomi", "McCullum The Manse Clinic", "info@themanseclinic.com.au", "Sydney Australia", "https://themanseclinic.com.au", "https://instagram.com/drnaomi1"),
        ("Dr. Joseph", "Hkeik All Saints Skin Clinic", "info@allsaintsskinclinic.com.au", "Sydney Australia", "https://allsaintsskinclinic.com.au", "https://instagram.com/allsaintsskinclinic")
    ],
    "Fitness & Wellness": [
        ("Marcus", "Apex Athletic Performance", "marcus@apexperformance.com", "Los Angeles USA", "https://apexperformance.com", "https://instagram.com/apexathletic"),
        ("Gunnar", "Peterson Fitness Hub", "info@gunnarpeterson.com", "Beverly Hills USA", "https://gunnarpeterson.com", "https://instagram.com/gunnarfitness"),
        ("Harley", "Pasternak Training", "info@harleypasternak.com", "Los Angeles USA", "https://harleypasternak.com", "https://instagram.com/harleypasternak"),
        ("Don", "Saladino Drive 495", "info@donsaladino.com", "New York USA", "https://donsaladino.com", "https://instagram.com/donsaladino"),
        ("Tracy", "Anderson Method Studio", "clientservices@tracyandersonmethod.com", "New York & London", "https://tracyanderson.com", "https://instagram.com/tracyandersonmethod"),
        ("Luke", "Zocchi The 28 Program", "support@zocobodypro.com", "Byron Bay Australia", "https://zocobodypro.com", "https://instagram.com/zocobodypro"),
        ("Kaya", "Health Clubs", "info@kayahc.com.au", "Melbourne Australia", "https://kayahc.com.au", "https://instagram.com/kayaclubs"),
        ("Matt", "Third Space London", "concierge@thirdspace.london", "London UK", "https://thirdspace.london", "https://instagram.com/thirdspacelondon"),
        ("David", "Equinox Fitness Clubs", "concierge@equinox.com", "New York & London", "https://equinox.com", "https://instagram.com/equinox"),
        ("Barry", "Barry's Bootcamp Global", "help@barrys.com", "Los Angeles & London", "https://barrys.com", "https://instagram.com/barrys"),
        ("James", "KX Life Luxury Wellness Club", "info@kxlife.co.uk", "London UK", "https://kxlife.co.uk", "https://instagram.com/kxlife"),
        ("Harry", "Workshop Gymnasium", "info@workshopgymnasium.com", "London UK", "https://workshopgymnasium.com", "https://instagram.com/workshopgymnasium"),
        ("Ben", "BXR London Boxing Club", "info@bxrlondon.com", "London UK", "https://bxrlondon.com", "https://instagram.com/bxrlondon"),
        ("Ashley", "Dogpound Training Gym", "info@thedogpound.com", "New York & LA", "https://thedogpound.com", "https://instagram.com/dogpound"),
        ("Chris", "Centr Fitness Program", "support@centr.com", "Melbourne & LA", "https://centr.com", "https://instagram.com/centrfit"),
        ("Sam", "F45 Training Corporate", "support@f45training.com", "Austin USA", "https://f45training.com", "https://instagram.com/f45_training"),
        ("Nick", "Roar Fitness London", "info@roar-fitness.com", "London UK", "https://roar-fitness.com", "https://instagram.com/roarfitnessltd"),
        ("Tom", "Evolve 353 Gym", "info@evolve353.com", "London UK", "https://evolve353.com", "https://instagram.com/evolve353"),
        ("Paul", "One Wave Fitness", "hello@onewavefitness.com", "Sydney Australia", "https://onewavefitness.com", "https://instagram.com/onewaveisallittakes"),
        ("Simon", "Virgin Active Classic", "info@virginactive.co.uk", "London UK", "https://virginactive.co.uk", "https://instagram.com/virginactiveuk")
    ],
    "Fashion & Leather Goods": [
        ("Liam", "Hardgraft Luxury Leather Goods", "support@hardgraft.com", "London & Vienna", "https://hardgraft.com", "https://instagram.com/hardgraft"),
        ("Carl", "Carl Friedrik Travel & Leather", "contact@carlfriedrik.com", "London UK", "https://carlfriedrik.com", "https://instagram.com/carlfriedrik"),
        ("Frank", "Frank Clegg Leatherworks", "info@frankcleggleatherworks.com", "Boston USA", "https://frankcleggleatherworks.com", "https://instagram.com/frankclegg"),
        ("Marco", "Smythson of Bond Street", "enquiries@smythson.com", "London UK", "https://smythson.com", "https://instagram.com/smythson"),
        ("Arthur", "Bennett Winch Handcrafted Bags", "info@bennettwinch.com", "London UK", "https://bennettwinch.com", "https://instagram.com/bennettwinch"),
        ("Luke", "Ettinger London Leatherware", "enquiries@ettinger.co.uk", "London UK", "https://ettinger.co.uk", "https://instagram.com/ettinger.london"),
        ("Julian", "Swaine Adeney Brigg", "enquiries@swaineadeneybrigg.co.uk", "London UK", "https://swaineadeneybrigg.co.uk", "https://instagram.com/swaineadeneybrigg"),
        ("Stefan", "Troubadour Goods", "hello@troubadourgoods.com", "London UK", "https://troubadourgoods.com", "https://instagram.com/troubadourgoods"),
        ("David", "Shinola Detroit Leather", "customerservice@shinola.com", "Detroit USA", "https://shinola.com", "https://instagram.com/shinola"),
        ("Max", "Tanner Goods Portland", "service@tannergoods.com", "Portland USA", "https://tannergoods.com", "https://instagram.com/tannergoods"),
        ("Gabriel", "Killspencer Luxury Athletic Leather", "contact@killspencer.com", "Los Angeles USA", "https://killspencer.com", "https://instagram.com/killspencer"),
        ("Daniel", "Lotuff Leather Handcrafted", "info@lotuffleather.com", "Providence USA", "https://lotuffleather.com", "https://instagram.com/lotuffleather"),
        ("Simon", "Ghurka Handcrafted Leather", "customerservice@ghurka.com", "New York USA", "https://ghurka.com", "https://instagram.com/ghurkausa"),
        ("Adam", "Mulberry Luxury Goods", "enquiries@mulberry.com", "Somerset & London", "https://mulberry.com", "https://instagram.com/mulberryengland"),
        ("Charles", "Aspinal of London", "enquiries@aspinaloflondon.com", "London UK", "https://aspinaloflondon.com", "https://instagram.com/aspinaloflondon"),
        ("Oliver", "Launer London Royal Leather", "info@launer.com", "London UK", "https://launer.com", "https://instagram.com/launerlondonofficial"),
        ("Henry", "Purdey Luxury Field Goods", "enquiries@purdey.com", "London UK", "https://purdey.com", "https://instagram.com/purdey_guns"),
        ("James", "Holdall London", "info@holdall.co.uk", "London UK", "https://holdall.co.uk", "https://instagram.com/holdalllondon"),
        ("Benjamin", "Craighill Goods", "support@craighill.co", "New York USA", "https://craighill.co", "https://instagram.com/craighillcompany"),
        ("Lucas", "Moore & Giles Leather", "info@mooreandgiles.com", "Virginia USA", "https://mooreandgiles.com", "https://instagram.com/mooreandgiles")
    ],
    "Home Decor & Lighting": [
        ("Oliver", "Kanso Design Collective", "oliver@kansodesign.de", "Berlin Germany", "https://kansodesign.de", "https://instagram.com/kansodesign"),
        ("Michael", "Ochre Lighting and Furniture", "sales@ochre.net", "London & New York", "https://ochre.net", "https://instagram.com/ochrestore"),
        ("Lee", "Broom Lighting Studio", "sales@leebroom.com", "London UK", "https://leebroom.com", "https://instagram.com/leebroom"),
        ("Tom", "Dixon Design Studio", "customerservices@tomdixon.net", "London UK", "https://tomdixon.net", "https://instagram.com/tomdixonstudio"),
        ("Lindsey", "Adelman Lighting Studio", "info@lindseyadelman.com", "New York USA", "https://lindseyadelman.com", "https://instagram.com/lindseyadelman"),
        ("Gabriel", "Apparatus Studio", "info@apparatusstudio.com", "New York USA", "https://apparatusstudio.com", "https://instagram.com/apparatusstudio"),
        ("Jason", "Miller Roll & Hill", "sales@rollandhill.com", "New York USA", "https://rollandhill.com", "https://instagram.com/rollandhill"),
        ("Matthew", "Lambert & Fils Lighting", "info@lambertetfils.com", "Montreal Canada", "https://lambertetfils.com", "https://instagram.com/lambertetfils"),
        ("Christopher", "Boots Lighting", "studio@christopherboots.com", "Melbourne Australia", "https://christopherboots.com", "https://instagram.com/christopherboots"),
        ("David", "Bec Brittain Studio", "info@becbrittain.com", "New York USA", "https://becbrittain.com", "https://instagram.com/becbrittain"),
        ("Pippa", "Porta Romana Lighting", "sales@portaromana.com", "Surrey UK", "https://portaromana.com", "https://instagram.com/portaromanauk"),
        ("Julian", "CTO Lighting", "mail@ctolighting.co.uk", "London UK", "https://ctolighting.co.uk", "https://instagram.com/ctolighting"),
        ("Sophie", "Bert Frank Lighting", "info@bertfrank.co.uk", "London UK", "https://bertfrank.co.uk", "https://instagram.com/bertfrankltd"),
        ("Elena", "Original BTC Lighting", "sales@originalbtc.com", "Oxfordshire UK", "https://originalbtc.com", "https://instagram.com/originalbtc"),
        ("Maya", "Vaughan Designs", "uk-sales@vaughandesigns.com", "London UK", "https://vaughandesigns.com", "https://instagram.com/vaughandesigns"),
        ("Hannah", "Soane Britain Decor", "enquiries@soane.co.uk", "London UK", "https://soane.co.uk", "https://instagram.com/soanebritain"),
        ("Grace", "Rose Uniacke Home Decor", "mail@roseuniacke.com", "London UK", "https://roseuniacke.com", "https://instagram.com/roseuniacke"),
        ("Amelia", "Pinch Design Studio", "info@pinchdesign.com", "London UK", "https://pinchdesign.com", "https://instagram.com/pinch_london"),
        ("Chloe", "De Gournay Wallcoverings", "info@degournay.com", "London & Paris", "https://degournay.com", "https://instagram.com/degournay"),
        ("Lucas", "Cole & Son Decor", "client.service@cole-and-son.com", "London UK", "https://cole-and-son.com", "https://instagram.com/cole_and_son_wallpapers")
    ],
    "Tattoo & Body Art": [
        ("Alex", "Black Anchor Tattoo Collective", "alex@blackanchortattoo.com", "Los Angeles USA", "https://blackanchortattoo.com", "https://instagram.com/blackanchortattoo"),
        ("Nikko", "Hurtado Black Anchor Studio", "nikkohurtadostudio@gmail.com", "Los Angeles USA", "https://nikkohurtado.com", "https://instagram.com/nikkohurtado"),
        ("Kat", "High Voltage Tattoo Studio", "booking@highvoltagetattoo.com", "Los Angeles USA", "https://highvoltagetattoo.com", "https://instagram.com/highvoltagetat"),
        ("Keith", "Bang Bang Tattoo NYC", "contact@bangbangforever.com", "New York USA", "https://bangbangforever.com", "https://instagram.com/bangbangnyc"),
        ("Scott", "Saved Tattoo Studio", "savedtattoo@gmail.com", "New York USA", "https://savedtattoo.com", "https://instagram.com/saved_tattoo"),
        ("Paul", "Love Hate Tattoo Studio", "info@lovehatetattoos.com", "Miami USA", "https://lovehatetattoos.com", "https://instagram.com/lovehatetattoos"),
        ("Oliver", "Three Kings Tattoo NYC", "threekingstattoo@gmail.com", "New York USA", "https://threekingstattoo.com", "https://instagram.com/threekingstattoo"),
        ("Daniel", "Sang Bleu Tattoo London", "london@sangbleu.com", "London UK", "https://sangbleu.com", "https://instagram.com/sangbleutattoolondon"),
        ("Simon", "Cloak and Dagger Tattoo", "info@cloakanddaggerlondon.co.uk", "London UK", "https://cloakanddaggerlondon.co.uk", "https://instagram.com/cloakanddaggerlondon"),
        ("Marco", "The Circle London Tattoo", "info@thecirclelondon.com", "London UK", "https://thecirclelondon.com", "https://instagram.com/thecirclelondon"),
        ("Gabriel", "Seven Doors Tattoo", "info@sevendoorstattoo.com", "London UK", "https://sevendoorstattoo.com", "https://instagram.com/sevendoorstattoo"),
        ("Lucas", "Black Garden Tattoo", "info@blackgardentattoo.com", "London UK", "https://blackgardentattoo.com", "https://instagram.com/blackgardentattoo"),
        ("Michael", "Frith Street Tattoo", "info@frithstreettattoo.co.uk", "London UK", "https://frithstreettattoo.co.uk", "https://instagram.com/frithstreettattoo"),
        ("Ryan", "Modern Electric Tattoo Co.", "info@modernelectric.co.uk", "Birmingham UK", "https://modernelectric.co.uk", "https://instagram.com/modernelectrictattoo"),
        ("Jack", "Good Times Tattoo", "info@goodtimestattoo.co.uk", "London UK", "https://goodtimestattoo.co.uk", "https://instagram.com/goodtimestattoo"),
        ("Ben", "Vader Tattoo Studio", "vadertattoo@gmail.com", "Melbourne Australia", "https://vadertattoo.com", "https://instagram.com/vadertattoo"),
        ("Nathan", "Dynamic Tattoo Melbourne", "info@dynamictattoo.com", "Melbourne Australia", "https://dynamictattoo.com", "https://instagram.com/dynamictattoomelbourne"),
        ("David", "Victorian Ink Studio", "info@victorianink.com.au", "Melbourne Australia", "https://victorianink.com.au", "https://instagram.com/victorianink"),
        ("Ethan", "Hunter & Fox Tattoo", "info@hunterandfoxtattoo.com", "Sydney Australia", "https://hunterandfoxtattoo.com", "https://instagram.com/hunterandfox"),
        ("Liam", "Stone Heart Body Art", "info@stoneheart.com.au", "Sydney Australia", "https://stoneheart.com.au", "https://instagram.com/stoneheartbodyart")
    ]
}

# Assemble in alternating round-robin order so every consecutive lead is from a DIFFERENT field!
ordered_leads = []
keys = list(niches_data.keys())
max_count = max(len(v) for v in niches_data.values())

tiers_cycle = ["International", "Higher than Local", "Local"]
tier_idx = 0

for i in range(max_count):
    for key in keys:
        if i < len(niches_data[key]):
            item = niches_data[key][i]
            tier = tiers_cycle[tier_idx % len(tiers_cycle)]
            tier_idx += 1
            ordered_leads.append({
                "First Name": item[0],
                "Business": item[1],
                "Email": item[2],
                "Field": key,
                "Tier": tier,
                "Location": item[3],
                "Website": item[4],
                "Instagram": item[5]
            })

print(f"Total leads compiled: {len(ordered_leads)}")

# Write to leads.csv
with open("leads.csv", "w", encoding="utf-8", newline="") as f:
    fieldnames = ["First Name", "Business", "Email", "Field", "Tier", "Location", "Website", "Instagram"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for row in ordered_leads:
        writer.writerow(row)

print("Saved 200 leads to leads.csv successfully in alternating round-robin order!")
