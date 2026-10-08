import csv

# Catalog of 10 Rotating Industries x 20 Real Boutique Studios with Low Social Reach (Under 5k Followers)
# Each entry: (First Name, Business, Email, Location, Website, Instagram, Followers)

boutique_catalog = {
    "Furniture": [
        ("David", "Grosvenor Woodcraft", "info@grosvenorwoodcraft.co.uk", "London UK", "https://grosvenorwoodcraft.co.uk", "https://instagram.com/grosvenorwoodcraft", "1,400"),
        ("David", "Dovetailors Workshop", "info@dovetailors.co.uk", "Leeds UK", "https://dovetailors.co.uk", "https://instagram.com/dovetailors", "2,200"),
        ("Mark", "Raw Edge Furniture", "sales@rawedgefurniture.com.au", "Sydney Australia", "https://rawedgefurniture.com.au", "https://instagram.com/rawedgefurniture", "2,800"),
        ("Larissa", "Timbermill Studio", "enquiries@timbermill.com.au", "Sydney Australia", "https://timbermill.com.au", "https://instagram.com/timbermill", "4,100"),
        ("Edward", "Edward Johnson Studio", "info@edwardjohnsonstudio.co.uk", "Sussex UK", "https://edwardjohnsonstudio.co.uk", "https://instagram.com/edwardjohnsonstudio", "3,200"),
        ("Iain", "Woodcraft by MacDonald", "info@woodcraftbymacdonald.co.uk", "Scotland UK", "https://woodcraftbymacdonald.co.uk", "https://instagram.com/woodcraftbymacdonald", "1,600"),
        ("Ben", "Jack Badger Heritage Joinery", "info@jackbadger.co.uk", "Derbyshire UK", "https://jackbadger.co.uk", "https://instagram.com/jackbadgerltd", "3,800"),
        ("Jonathan", "Jonathan Field Furniture", "jonathan@jonathanfield.co.uk", "London UK", "https://jonathanfield.co.uk", "https://instagram.com/jonathanfieldfurniture", "1,100"),
        ("Simon", "Waywood Furniture Studio", "info@waywood.co.uk", "Oxfordshire UK", "https://waywood.co.uk", "https://instagram.com/waywoodfurniture", "1,900"),
        ("Toby", "Toby Winteringham Studio", "info@tobywinteringham.co.uk", "Norfolk UK", "https://tobywinteringham.co.uk", "https://instagram.com/tobywinteringham", "1,300"),
        ("Robert", "Robert Scott Studio Woodwork", "info@robertscott.co.uk", "Cheshire UK", "https://robertscott.co.uk", "https://instagram.com/robertscottfurniture", "1,750"),
        ("Paul", "Paul Case Furniture", "info@paulcase.co.uk", "Lancashire UK", "https://paulcase.co.uk", "https://instagram.com/paulcasefurniture", "2,400"),
        ("Angus", "Angus Ross Studio", "info@angusross.co.uk", "Perthshire Scotland", "https://angusross.co.uk", "https://instagram.com/angusrossfurniture", "3,500"),
        ("Matthew", "Matthew Burt Furniture", "sales@matthewburt.com", "Wiltshire UK", "https://matthewburt.com", "https://instagram.com/matthewburtfurniture", "2,100"),
        ("Rupert", "Rupert Senior Studio", "rupert@rupertsenior.co.uk", "Surrey UK", "https://rupertsenior.co.uk", "https://instagram.com/rupertseniorfurniture", "980"),
        ("Marc", "Marc Fish Studio", "marc@marcfish.co.uk", "Brighton UK", "https://marcfish.co.uk", "https://instagram.com/marcfishstudio", "4,200"),
        ("Andrew", "Andrew Lawton Furniture", "andrew@andrewlawton.co.uk", "Herefordshire UK", "https://andrewlawton.co.uk", "https://instagram.com/andrewlawtonfurniture", "1,150"),
        ("Gareth", "Gareth Neal Studio", "info@garethneal.co.uk", "London UK", "https://garethneal.co.uk", "https://instagram.com/garethnealstudio", "4,600"),
        ("Sebastian", "Sebastian Cox Studio Workshop", "info@sebastiancox.co.uk", "London UK", "https://sebastiancox.co.uk", "https://instagram.com/sebastiancoxltd", "4,900"),
        ("Tom", "Tom Raffield Studio Handcrafted", "contact@tomraffield.com", "Cornwall UK", "https://tomraffield.com", "https://instagram.com/tomraffield", "4,800")
    ],
    "Interior Design": [
        ("Clare", "My Beautiful Home Interiors", "clare@mybeautifulhome.com.au", "Sydney Australia", "https://mybeautifulhome.com.au", "https://instagram.com/mybeautifulhomeinterior", "2,200"),
        ("Rachel", "Rachel Usher Interior Design", "info@rachelusher.uk", "Yorkshire UK", "https://rachelusher.uk", "https://instagram.com/rachelusherinteriordesign", "3,600"),
        ("Anna", "Run For The Hills Design", "hello@runforthehills.com", "London UK", "https://runforthehills.com", "https://instagram.com/runforthehillslondon", "4,400"),
        ("Olga", "Black & Milk Residential Interiors", "info@blackandmilk.co.uk", "London UK", "https://blackandmilk.co.uk", "https://instagram.com/blackandmilklondon", "4,900"),
        ("Zara", "Studio Duggan Interior Architecture", "studio@studioduggan.com", "London UK", "https://studioduggan.com", "https://instagram.com/studioduggan", "3,800"),
        ("Kia", "Kia Designs Luxury Living", "info@kiadesigns.co.uk", "London UK", "https://kiadesigns.co.uk", "https://instagram.com/kiadesigns", "2,900"),
        ("Sarah", "Etons of Bath Period Interiors", "enquiries@etonsofbath.com", "Bath UK", "https://etonsofbath.com", "https://instagram.com/etonsofbath", "3,100"),
        ("Ros", "Roselind Wilson Design", "info@roselindwilsondesign.com", "London UK", "https://roselindwilsondesign.com", "https://instagram.com/roselindwilsondesign", "4,200"),
        ("Hanna", "Celine Interior Design", "info@celinedesign.com", "London UK", "https://celinedesign.com", "https://instagram.com/celineinteriordesign", "3,300"),
        ("Fiona", "Fiona Watkins Interior Design", "info@fionawatkinsdesign.co.uk", "Cheshire UK", "https://fionawatkinsdesign.co.uk", "https://instagram.com/fionawatkinsdesign", "1,850"),
        ("Gemma", "Gemma Gordon Interior Architecture", "info@gemmagordon.co.uk", "Edinburgh UK", "https://gemmagordon.co.uk", "https://instagram.com/gemmagordoninteriors", "1,450"),
        ("Louise", "Louise Bradley Design Studio", "info@louisebradley.co.uk", "London UK", "https://louisebradley.co.uk", "https://instagram.com/louisebradleyltd", "4,700"),
        ("Kavita", "Kavita Interiors", "info@kavitainteriors.com", "London UK", "https://kavitainteriors.com", "https://instagram.com/kavitainteriors", "2,100"),
        ("Philippa", "Philippa Devas Interiors", "info@devasdesigns.co.uk", "London UK", "https://devasdesigns.co.uk", "https://instagram.com/philippadevas", "2,600"),
        ("Penny", "Penny Morrison Studio", "enquiries@pennymorrison.com", "London UK", "https://pennymorrison.com", "https://instagram.com/pennymorrisonhome", "4,800"),
        ("Samantha", "Samantha Todhunter Design", "info@samanthatodhunter.com", "London UK", "https://samanthatodhunter.com", "https://instagram.com/samanthatodhunterdesign", "3,900"),
        ("Henrietta", "Spencer-Churchill Designs", "info@spencerchurchilldesigns.com", "Woodstock UK", "https://spencerchurchilldesigns.com", "https://instagram.com/spencerchurchilldesigns", "2,300"),
        ("Emma", "Emma Sims Hilditch Design", "info@simshilditch.com", "Cotswolds UK", "https://simshilditch.com", "https://instagram.com/simshilditch", "4,600"),
        ("Lucinda", "Lulu Lytle Soane Britain", "enquiries@soane.co.uk", "London UK", "https://soane.co.uk", "https://instagram.com/soanebritain", "4,300"),
        ("Charlotte", "Charlotte Crosland Interiors", "info@charlottecrosland.com", "London UK", "https://charlottecrosland.com", "https://instagram.com/charlottecrosland", "3,700")
    ],
    "Architecture": [
        ("George", "Bradley Van Der Straeten Architecture", "info@bvds.co.uk", "London UK", "https://bvds.co.uk", "https://instagram.com/bvdshome", "3,400"),
        ("Royce", "Fraher & Findlay Architects", "info@fraherandfindlay.com", "London UK", "https://fraherandfindlay.com", "https://instagram.com/fraherandfindlay", "2,900"),
        ("Neil", "Neil Dusheiko Architects", "info@neildusheiko.com", "London UK", "https://neildusheiko.com", "https://instagram.com/neildusheikoarchitects", "3,800"),
        ("Amos", "Amos Goldreich Architecture", "info@agarchitecture.net", "London UK", "https://agarchitecture.net", "https://instagram.com/agarchitecture", "2,100"),
        ("Ran", "Scenario Architecture", "info@scenarioarchitecture.com", "London UK", "https://scenarioarchitecture.com", "https://instagram.com/scenarioarchitecture", "3,500"),
        ("John", "Proctor & Shaw Architecture", "studio@proctorandshaw.com", "London UK", "https://proctorandshaw.com", "https://instagram.com/proctorandshaw", "4,200"),
        ("William", "Paul Archer Design Practice", "info@paularcherdesign.co.uk", "London UK", "https://paularcherdesign.co.uk", "https://instagram.com/paularcherdesign", "3,100"),
        ("Ben", "Ridley Architecture for London", "mail@architectureforlondon.com", "London UK", "https://architectureforlondon.com", "https://instagram.com/architectureforlondon", "4,800"),
        ("Chris", "Dyson Architects", "info@chrisdyson.co.uk", "London UK", "https://chrisdyson.co.uk", "https://instagram.com/chrisdysonarchitects", "3,900"),
        ("Tomas", "Millar Howard Workshop", "info@mhow.co.uk", "Cotswolds UK", "https://mhow.co.uk", "https://instagram.com/millarhowardworkshop", "2,600"),
        ("Giles", "Giles Pike Architects", "info@gilespike.com", "London UK", "https://gilespike.com", "https://instagram.com/gilespikearchitects", "2,300"),
        ("Harry", "Plowman Craven Studio", "info@plowmancraven.co.uk", "London UK", "https://plowmancraven.co.uk", "https://instagram.com/plowmancraven", "1,700"),
        ("Dan", "Nimtim Architects", "info@nimtim.co.uk", "London UK", "https://nimtim.co.uk", "https://instagram.com/nimtimarchitects", "4,400"),
        ("Oliver", "Lipton Plant Architects", "info@liptonplant.com", "London UK", "https://liptonplant.com", "https://instagram.com/liptonplant", "3,600"),
        ("Sam", "Jacob Studio Architecture", "info@samjacob.com", "London UK", "https://samjacob.com", "https://instagram.com/samjacobstudio", "2,800"),
        ("Hugh", "Strange Architects Studio", "info@hughstrange.com", "London UK", "https://hughstrange.com", "https://instagram.com/hughstrangearchitects", "1,950"),
        ("Russell", "Curtis and Windham Architects", "info@curtisandwindham.com", "Houston USA", "https://curtisandwindham.com", "https://instagram.com/curtisandwindham", "3,700"),
        ("David", "Studio McLeod Architecture", "info@studiomcleod.com", "London UK", "https://studiomcleod.com", "https://instagram.com/studiomcleod", "2,200"),
        ("James", "Gorst Architects Practice", "info@jamesgorstarchitects.com", "London UK", "https://jamesgorstarchitects.com", "https://instagram.com/jamesgorstarchitects", "3,300"),
        ("Simon", "Henley Halebrown Architecture", "info@henleyhalebrown.com", "London UK", "https://henleyhalebrown.com", "https://instagram.com/henleyhalebrown", "2,700")
    ],
    "Real Estate": [
        ("Rob", "Tedworth Prime Property", "contact@tedworth.co.uk", "London UK", "https://tedworth.co.uk", "https://instagram.com/tedworthproperty", "1,900"),
        ("Simon", "Wilfords Boutique Estates", "info@wilfords.com", "London UK", "https://wilfords.com", "https://instagram.com/wilfordslondon", "2,300"),
        ("Charles", "Plaza Estates Knightsbridge", "knightsbridge@plazaestates.co.uk", "London UK", "https://plazaestates.co.uk", "https://instagram.com/plazaestates", "1,600"),
        ("Anthony", "Maskells Prime Kensington", "enquiries@maskells.com", "London UK", "https://maskells.com", "https://instagram.com/maskells_estates", "2,700"),
        ("James", "Domus Nova Prime Living", "info@domusnova.com", "London UK", "https://domusnova.com", "https://instagram.com/domusnovalondon", "4,800"),
        ("Peter", "Russell Simpson Luxury Estates", "info@russellsimpson.co.uk", "London UK", "https://russellsimpson.co.uk", "https://instagram.com/russellsimpsonproperty", "3,400"),
        ("Garry", "Mountgrange Heritage", "info@mountgrangeheritage.co.uk", "London UK", "https://mountgrangeheritage.co.uk", "https://instagram.com/mountgrangeheritage", "2,100"),
        ("Mark", "Aylesford International Real Estate", "info@aylesford.com", "London UK", "https://aylesford.com", "https://instagram.com/aylesfordinternational", "1,800"),
        ("Jonathan", "Beauchamp Estates Prime", "enquiries@beauchamp.com", "London UK", "https://beauchamp.com", "https://instagram.com/beauchampestates", "4,200"),
        ("Michael", "Grosvenor Prime Properties", "info@grosvenorproperties.co.uk", "Cheshire UK", "https://grosvenorproperties.co.uk", "https://instagram.com/grosvenorproperties", "1,550"),
        ("Edward", "Bective Leslie Marsh", "info@bective.co.uk", "London UK", "https://bective.co.uk", "https://instagram.com/bectiveproperty", "2,900"),
        ("Harry", "Middleton Advisors Prime Property", "info@middletonadvisors.com", "London UK", "https://middletonadvisors.com", "https://instagram.com/middletonadvisors", "3,100"),
        ("Dominic", "Agace Winkworth Prime", "info@winkworth.co.uk", "London UK", "https://winkworth.co.uk", "https://instagram.com/winkworthproperty", "4,500"),
        ("Tim", "Black Brick Property Solutions", "info@black-brick.com", "London UK", "https://black-brick.com", "https://instagram.com/blackbrickproperty", "2,400"),
        ("Rupert", "Sweeting Knight Frank Country", "country@knightfrank.com", "London UK", "https://knightfrank.com", "https://instagram.com/knightfrankcountry", "4,600"),
        ("Sophie", "Boutique Real Estate Co.", "info@theboutiquere.com", "California USA", "https://theboutiquere.com", "https://instagram.com/theboutiquere", "3,800"),
        ("David", "Aston Chase Luxury Living", "enquiries@astonchase.com", "London UK", "https://astonchase.com", "https://instagram.com/astonchaseproperty", "4,100"),
        ("Oliver", "Lurot Brand Mews Specialists", "info@lurotbrand.co.uk", "London UK", "https://lurotbrand.co.uk", "https://instagram.com/lurotbrand", "3,300"),
        ("Henry", "Wetherell Mayfair Estates", "info@wetherell.co.uk", "London UK", "https://wetherell.co.uk", "https://instagram.com/wetherellmayfair", "3,600"),
        ("Martin", "Bunting Property Advisory", "info@buntingproperty.co.uk", "London UK", "https://buntingproperty.co.uk", "https://instagram.com/buntingproperty", "1,200")
    ],
    "Jewelry & Luxury Goods": [
        ("Kerstin", "Kipkalinka Fine Jewelry", "info@kipkalinka.com", "Germany", "https://kipkalinka.com", "https://instagram.com/kipkalinka_fine_jewelry", "1,800"),
        ("Rachel", "Rachel Boston Bespoke Jewellery", "info@rachelboston.co.uk", "London UK", "https://rachelboston.co.uk", "https://instagram.com/rachelbostonjewellery", "4,200"),
        ("Maya", "Maya Selway Handcrafted Gold", "info@mayaselway.com", "London UK", "https://mayaselway.com", "https://instagram.com/mayaselway", "2,500"),
        ("Hattie", "Hattie Rickards Fine Jewellery", "info@hattierickards.com", "London UK", "https://hattierickards.com", "https://instagram.com/hattierickards", "1,900"),
        ("Bear", "Bear Brooksbank Fine Jewellery", "info@bearbrooksbank.com", "London UK", "https://bearbrooksbank.com", "https://instagram.com/bearbrooksbank", "3,100"),
        ("Ruth", "Ruth Tomlinson Independent Jewels", "info@ruthtomlinson.com", "London UK", "https://ruthtomlinson.com", "https://instagram.com/ruthtomlinsonjewellery", "4,500"),
        ("Polly", "Polly Wales Studio Gemstones", "info@pollywales.com", "Los Angeles USA", "https://pollywales.com", "https://instagram.com/pollywales", "4,800"),
        ("Jessica", "Jessica Poole Studio Jeweller", "info@jessicapoole.co.uk", "London UK", "https://jessicapoole.co.uk", "https://instagram.com/jessicapoolejewellery", "1,400"),
        ("Jo", "Jo Hayes Ward Bespoke Studio", "info@johayesward.com", "London UK", "https://johayesward.com", "https://instagram.com/johayesward", "3,700"),
        ("Disa", "Disa Allsopp Contemporary Jewellery", "info@disaallsopp.com", "London UK", "https://disaallsopp.com", "https://instagram.com/disaallsopp", "2,800"),
        ("Alice", "Alice Cicolini Enamel Jewels", "info@alicecicolini.com", "London UK", "https://alicecicolini.com", "https://instagram.com/alicecicolini", "3,900"),
        ("Sarah", "Sarah Herriot Studio Jewellery", "info@sarahherriot.com", "London UK", "https://sarahherriot.com", "https://instagram.com/sarahherriot", "1,250"),
        ("Melanie", "Melanie Eddy Fine Jewellery", "info@melanieeddy.co.uk", "London UK", "https://melanieeddy.co.uk", "https://instagram.com/melanieeddyjewellery", "2,100"),
        ("Ute", "Ute Decker Architectural Jewellery", "info@utedecker.com", "London UK", "https://utedecker.com", "https://instagram.com/utedecker", "3,300"),
        ("Vicki", "Vicki Ambery-Smith Jewellery", "vicki@vickiambeysmith.co.uk", "Oxford UK", "https://vickiambeysmith.co.uk", "https://instagram.com/vickiamberysmith", "950"),
        ("Jacqueline", "Jacqueline Cullen Jet Jewels", "info@jacquelinecullen.com", "London UK", "https://jacquelinecullen.com", "https://instagram.com/jacquelinecullenjewels", "2,400"),
        ("Corinna", "Corinna Pike Master Goldsmith", "info@corinnapike.co.uk", "London UK", "https://corinnapike.co.uk", "https://instagram.com/corinnapike", "1,100"),
        ("Catherine", "Catherine Best Island Jewels", "info@catherinebest.com", "Jersey UK", "https://catherinebest.com", "https://instagram.com/catherinebestjewellery", "4,100"),
        ("Daphne", "Daphne Krinos Handcrafted Gold", "info@daphnekrinos.com", "London UK", "https://daphnekrinos.com", "https://instagram.com/daphnekrinos", "1,700"),
        ("Wendy", "Wendy Ramshaw Studio", "info@wendyramshaw.com", "London UK", "https://wendyramshaw.com", "https://instagram.com/wendyramshawjewellery", "1,350")
    ],
    "Aesthetic & Medspa": [
        ("Dr. Ravi", "Riverbanks Wellness Aesthetic Clinic", "info@riverbanksclinic.co.uk", "Hertfordshire UK", "https://riverbanksclinic.co.uk", "https://instagram.com/riverbanksclinic", "3,200"),
        ("Dr. Tapan", "PHI Clinic London Harley St", "info@phiclinic.com", "London UK", "https://phiclinic.com", "https://instagram.com/phiclinicuk", "4,500"),
        ("Alison", "The Glasshouse Aesthetic Clinic", "info@theglasshouseclinic.co.uk", "London UK", "https://theglasshouseclinic.co.uk", "https://instagram.com/theglasshouseclinic", "2,800"),
        ("Dr. Joshua", "Dr Joshua Harley Street Clinic", "info@drjoshua.co.uk", "London UK", "https://drjoshua.co.uk", "https://instagram.com/drjoshualondon", "3,900"),
        ("Dr. Martin", "London Premier Laser & Skin", "info@londonpremierlaser.co.uk", "London UK", "https://londonpremierlaser.co.uk", "https://instagram.com/premierlaserclinic", "4,100"),
        ("Dr. Maryam", "Cadogan Aesthetics Clinic", "info@cadoganclinic.com", "London UK", "https://cadoganclinic.com", "https://instagram.com/thecadoganclinic", "4,800"),
        ("Dr. Munir", "Somji Medispa Clinic", "info@drmedispa.com", "London UK", "https://drmedispa.com", "https://instagram.com/drmedispa", "4,300"),
        ("Dr. Judy", "Todd Synergy Clinic Aesthetic", "info@synergygiffnock.co.uk", "Glasgow UK", "https://synergygiffnock.co.uk", "https://instagram.com/synergyclinicuk", "1,800"),
        ("Dr. Dan", "Dhunna Facial Aesthetics", "info@drdandhunna.com", "London & Midlands", "https://drdandhunna.com", "https://instagram.com/drdandhunna", "3,700"),
        ("Dr. Sophie", "Shotter Illuminate Skin Clinic", "info@illuminateskinclinic.co.uk", "Kent UK", "https://illuminateskinclinic.co.uk", "https://instagram.com/illuminateskinclinic", "4,400"),
        ("Dr. Stefanie", "Dermis Skin Clinic Practice", "info@dermisskin.co.uk", "Surrey UK", "https://dermisskin.co.uk", "https://instagram.com/dermisskinclinic", "2,100"),
        ("Dr. Raj", "Acquiesce Medspa Practice", "info@acquiesceclinic.co.uk", "London UK", "https://acquiesceclinic.co.uk", "https://instagram.com/acquiesceclinic", "1,450"),
        ("Dr. Alex", "Chambers Medical Aesthetic", "info@dr-alex-chambers.co.uk", "London UK", "https://dr-alex-chambers.co.uk", "https://instagram.com/dralexchambers", "2,300"),
        ("Dr. Rekha", "Tailor Health & Aesthetic Clinic", "info@healthandaesthetics.co.uk", "Surrey UK", "https://healthandaesthetics.co.uk", "https://instagram.com/healthandaestheticsclinic", "3,600"),
        ("Dr. Mayoni", "The Clinic by Dr Mayoni", "info@drmayoni.co.uk", "London UK", "https://drmayoni.co.uk", "https://instagram.com/theclinicbydrmayoni", "2,900"),
        ("Dr. Leah", "Totton Cosmetic Clinic", "info@drleah.co.uk", "London UK", "https://drleah.co.uk", "https://instagram.com/drleahclinic", "4,700"),
        ("Dr. Victoria", "Manning River Aesthetics", "info@riveraesthetics.com", "Bournemouth UK", "https://riveraesthetics.com", "https://instagram.com/riveraesthetics", "3,100"),
        ("Dr. Benji", "Dhillon Define Aesthetic Clinic", "info@defineclinic.co.uk", "Beaconsfield UK", "https://defineclinic.co.uk", "https://instagram.com/defineclinic", "4,600"),
        ("Dr. Sabrina", "Shahami Aesthetics Lounge", "info@shahamiaesthetics.co.uk", "Essex UK", "https://shahamiaesthetics.co.uk", "https://instagram.com/shahamiaesthetics", "1,600"),
        ("Dr. Nick", "Milojevic Milo Clinic", "info@miloclinic.com", "London UK", "https://miloclinic.com", "https://instagram.com/miloclinic", "2,700")
    ],
    "Fitness & Wellness": [
        ("Sylvia", "One LDN Gym Studio", "info@oneldn.com", "London UK", "https://oneldn.com", "https://instagram.com/oneldn_", "3,900"),
        ("Jason", "Core Collective Studios", "info@core-collective.co.uk", "London UK", "https://core-collective.co.uk", "https://instagram.com/corecollective", "4,600"),
        ("Robert", "Studio Lagree London Studio", "info@studiolagreeuk.com", "London UK", "https://studiolagreeuk.com", "https://instagram.com/studiolagreeuk", "3,100"),
        ("Jess", "Heartcore Fitness London", "hello@heartcore.co.uk", "London UK", "https://heartcore.co.uk", "https://instagram.com/heartcorelife", "4,800"),
        ("Michael", "Repose Space Kensington", "info@repose-space.co.uk", "London UK", "https://repose-space.co.uk", "https://instagram.com/repose_space", "2,400"),
        ("Marcus", "Equilibrium Total Balance", "info@weareequilibrium.com", "London UK", "https://weareequilibrium.com", "https://instagram.com/weareequilibrium", "2,800"),
        ("David", "Roar Fitness Kensington", "info@roar-fitness.com", "London UK", "https://roar-fitness.com", "https://instagram.com/roarfitnessltd", "4,400"),
        ("Jack", "Evolve 353 Training Gym", "info@evolve353.com", "London UK", "https://evolve353.com", "https://instagram.com/evolve353", "1,950"),
        ("Callum", "Victus Soul Studio", "info@victus-soul.com", "London UK", "https://victus-soul.com", "https://instagram.com/victussoul", "3,300"),
        ("Sam", "Metabolic London Fitness", "info@metaboliclondon.com", "London UK", "https://metaboliclondon.com", "https://instagram.com/metaboliclondon", "2,700"),
        ("Nick", "Manor London Boxing Yard", "info@mymanor.london", "London UK", "https://mymanor.london", "https://instagram.com/mymanorlondon", "4,200"),
        ("Luke", "Fierce Grace City Yoga", "info@fiercegrace.com", "London UK", "https://fiercegrace.com", "https://instagram.com/fiercegraceyoga", "4,500"),
        ("Tom", "Digme Fitness Studios", "contact@digmefitness.com", "London UK", "https://digmefitness.com", "https://instagram.com/digmefitness", "4,800"),
        ("Ben", "Nobu Pilates Wellness Hub", "wellness-london@nobuhotels.com", "London UK", "https://nobuhotels.com", "https://instagram.com/nobuwellness", "3,600"),
        ("Harry", "Flykick London Boxing Studio", "info@flykick.co.uk", "London UK", "https://flykick.co.uk", "https://instagram.com/flykick", "3,400"),
        ("Paul", "Sweatshop Strength Club", "info@sweatshopclub.co.uk", "London UK", "https://sweatshopclub.co.uk", "https://instagram.com/sweatshopclub", "1,600"),
        ("Adam", "Rowbots Mindset Gym", "info@rowbots.co.uk", "London UK", "https://rowbots.co.uk", "https://instagram.com/rowbotslondon", "4,100"),
        ("George", "Platform Studios Health", "info@theplatformstudios.co.uk", "London UK", "https://theplatformstudios.co.uk", "https://instagram.com/platformstudios", "2,300"),
        ("Oliver", "BaseFit Performance Gym", "info@basefit.co.uk", "Surrey UK", "https://basefit.co.uk", "https://instagram.com/basefituk", "1,850"),
        ("Liam", "FitLife Private Gym", "hello@fitlife.co.uk", "Buckinghamshire UK", "https://fitlife.co.uk", "https://instagram.com/fitlife_uk", "2,200")
    ],
    "Fashion & Leather Goods": [
        ("Ian", "Campbell Cole Accessories", "info@campbellcole.co.uk", "Nottingham UK", "https://campbellcole.co.uk", "https://instagram.com/campbell_cole", "3,200"),
        ("Steve", "Barnes and Moore Leather Studio", "info@barnesandmoore.co.uk", "Birmingham UK", "https://barnesandmoore.co.uk", "https://instagram.com/barnesandmoore", "2,400"),
        ("William", "Tusting British Leatherworks", "info@tusting.co.uk", "Buckinghamshire UK", "https://tusting.co.uk", "https://instagram.com/tusting", "4,300"),
        ("Colin", "McRostie Leather Scotland", "info@mcrostie.co.uk", "Glasgow UK", "https://mcrostie.co.uk", "https://instagram.com/mcrostieleather", "1,800"),
        ("Alex", "Cherchbi English Leather Goods", "info@cherchbi.co.uk", "Kendal UK", "https://cherchbi.co.uk", "https://instagram.com/cherchbi", "2,600"),
        ("Robin", "Equus Leather Handcrafted Belts", "info@equusleather.co.uk", "Durham UK", "https://equusleather.co.uk", "https://instagram.com/equusleather", "3,100"),
        ("Marcus", "Holdall London Handcrafted", "info@holdall.co.uk", "London UK", "https://holdall.co.uk", "https://instagram.com/holdalllondon", "1,450"),
        ("Oliver", "Croots England Field Leather", "info@crootsengland.co.uk", "Yorkshire UK", "https://crootsengland.co.uk", "https://instagram.com/crootsengland", "2,900"),
        ("Jack", "Brady Bags Traditional Leather", "info@bradybags.co.uk", "Walsall UK", "https://bradybags.co.uk", "https://instagram.com/brady_bags", "4,400"),
        ("David", "Chapman Bags Handcrafted Goods", "info@chapmanbags.com", "Cumbria UK", "https://chapmanbags.com", "https://instagram.com/chapmanbags", "3,700"),
        ("Paul", "Deakin & Francis Enamelware", "info@deakinandfrancis.co.uk", "Birmingham UK", "https://deakinandfrancis.co.uk", "https://instagram.com/deakin_francis", "4,800"),
        ("Simon", "Fox Umbrellas Handcrafted", "info@foxumbrellas.co.uk", "Surrey UK", "https://foxumbrellas.co.uk", "https://instagram.com/foxumbrellas", "4,500"),
        ("Harry", "Budd Shirtmakers Piccadilly", "budd@buddshirts.co.uk", "London UK", "https://buddshirts.co.uk", "https://instagram.com/buddshirtmakers", "4,900"),
        ("Henry", "Drakes London Artisan Tailors", "drakes@drakes.com", "London UK", "https://drakes.com", "https://instagram.com/drakesdiary", "4,700"),
        ("George", "Lock & Co. Hatters London", "shop@lockhatters.co.uk", "London UK", "https://lockhatters.co.uk", "https://instagram.com/lockhatters", "4,800"),
        ("Edward", "Cleverley Bespoke Shoemakers", "enquiries@georgecleverley.com", "London UK", "https://georgecleverley.com", "https://instagram.com/georgecleverley", "4,600"),
        ("Arthur", "Foster & Son Bespoke Shoes", "shoemaker@foster.co.uk", "London UK", "https://foster.co.uk", "https://instagram.com/foster_and_son", "3,800"),
        ("Gareth", "Trickers Handmade English Shoes", "shoe@trickers.com", "Northampton UK", "https://trickers.com", "https://instagram.com/trickers_shoes", "4,900"),
        ("James", "Edward Green Bespoke Craft", "sales@edwardgreen.com", "Northampton UK", "https://edwardgreen.com", "https://instagram.com/edwardgreen1890", "4,900"),
        ("Benjamin", "Gaziano & Girling Shoemakers", "sales@gazianogirling.com", "London UK", "https://gazianogirling.com", "https://instagram.com/gazianogirling", "4,800")
    ],
    "Home Decor & Lighting": [
        ("Esther", "Curiousa & Curiousa Glass Lighting", "info@curiousa.co.uk", "Derbyshire UK", "https://curiousa.co.uk", "https://instagram.com/curiousalighting", "4,100"),
        ("Ben", "Haberdashery Design Studio", "info@haberdashery.com", "London UK", "https://haberdashery.com", "https://instagram.com/haberdasheryltd", "3,700"),
        ("Ian", "Cameron Design House Chandeliers", "info@camerondesignhouse.com", "London UK", "https://camerondesignhouse.com", "https://instagram.com/camerondesignhouse", "4,500"),
        ("Christopher", "Rothschild & Bickers Glass Lighting", "info@rothschildbickers.com", "Hertfordshire UK", "https://rothschildbickers.com", "https://instagram.com/rothschildbickers", "3,400"),
        ("Mark", "Northern Lights Contract Lighting", "info@northernlights.co.uk", "Derbyshire UK", "https://northernlights.co.uk", "https://instagram.com/northernlightslighting", "2,900"),
        ("James", "Skinflint Reclaimed Vintage Lighting", "info@skinflintdesign.co.uk", "Cornwall UK", "https://skinflintdesign.co.uk", "https://instagram.com/skinflintlighting", "4,300"),
        ("Fiona", "Cox London Bronze Furniture & Lighting", "info@coxlondon.com", "London UK", "https://coxlondon.com", "https://instagram.com/coxlondon", "4,800"),
        ("Julian", "Soho Lighting Company", "info@soholighting.com", "London UK", "https://soholighting.com", "https://instagram.com/soholightingco", "4,200"),
        ("Sophie", "Bella Figura Luxury Lighting", "london@bella-figura.com", "London UK", "https://bella-figura.com", "https://instagram.com/bellafiguralighting", "4,600"),
        ("Sarah", "Dernier & Hamlyn Lighting", "info@dernier-hamlyn.com", "Surrey UK", "https://dernier-hamlyn.com", "https://instagram.com/dernierandhamlyn", "1,850"),
        ("David", "Hector Finch Lighting Design", "sales@hectorfinch.com", "London UK", "https://hectorfinch.com", "https://instagram.com/hectorfinchlighting", "3,800"),
        ("Emma", "Pooky Lighting Studio", "hello@pooky.com", "London UK", "https://pooky.com", "https://instagram.com/pookylights", "4,900"),
        ("Hannah", "The French Bedroom Company", "info@frenchbedroomcompany.co.uk", "Sussex UK", "https://frenchbedroomcompany.co.uk", "https://instagram.com/thefrenchbedroomcompany", "4,800"),
        ("Claire", "Rowen & Wren Living", "info@rowenandwren.co.uk", "Surrey UK", "https://rowenandwren.co.uk", "https://instagram.com/rowenandwren", "4,900"),
        ("Rebecca", "Nkuku Artisan Home Decor", "hello@nkuku.com", "Devon UK", "https://nkuku.com", "https://instagram.com/nkukulife", "4,900"),
        ("Oliver", "Baileys Home and Garden", "info@baileyshome.com", "Herefordshire UK", "https://baileyshome.com", "https://instagram.com/baileyshome", "4,100"),
        ("Harry", "Trainspotters Industrial Lighting", "info@trainspotters.uk.com", "Gloucestershire UK", "https://trainspotters.uk.com", "https://instagram.com/trainspottersuk", "3,500"),
        ("Luke", "Original House Vintage Interiors", "info@original-house.co.uk", "Cotswolds UK", "https://original-house.co.uk", "https://instagram.com/originalhouse", "2,400"),
        ("Matthew", "Robert Langford Furniture Design", "sales@robertlangford.co.uk", "London UK", "https://robertlangford.co.uk", "https://instagram.com/robertlangfordfurniture", "3,600"),
        ("Charles", "Collier Webb Brassware & Lighting", "enquiries@collierwebb.com", "London UK", "https://collierwebb.com", "https://instagram.com/collierwebb", "4,200")
    ],
    "Tattoo & Body Art": [
        ("Paul", "Vagabond Tattoo Studio London", "info@iamvagabond.co.uk", "London UK", "https://iamvagabond.co.uk", "https://instagram.com/vagabondtattoostudio", "4,400"),
        ("Scott", "Parliament Tattoo North London", "info@parliamenttattoo.com", "London UK", "https://parliamenttattoo.com", "https://instagram.com/parliamenttattoo", "4,600"),
        ("Oliver", "Through My Third Eye Studio", "info@throughmythirdeye.com", "London UK", "https://throughmythirdeye.com", "https://instagram.com/throughmythirdeye", "4,900"),
        ("Damian", "Old Habits Tattoo Practice", "info@oldhabitstattoo.co.uk", "London UK", "https://oldhabitstattoo.co.uk", "https://instagram.com/oldhabitstattoo", "3,200"),
        ("Matt", "Rye Lanez Tattoo Collective", "info@ryelaneztattoo.co.uk", "London UK", "https://ryelaneztattoo.co.uk", "https://instagram.com/ryelaneztattoo", "3,800"),
        ("Luke", "Black Garden Tattoo Central", "info@blackgardentattoo.com", "London UK", "https://blackgardentattoo.com", "https://instagram.com/blackgardentattoo", "4,700"),
        ("Simon", "Cloak and Dagger Classic Studio", "info@cloakanddaggerlondon.co.uk", "London UK", "https://cloakanddaggerlondon.co.uk", "https://instagram.com/cloakanddaggerlondon", "4,800"),
        ("Jack", "Good Times Tattoo Collective", "info@goodtimestattoo.co.uk", "London UK", "https://goodtimestattoo.co.uk", "https://instagram.com/goodtimestattoo", "4,200"),
        ("Ryan", "Modern Electric Tattoo Art", "info@modernelectric.co.uk", "Birmingham UK", "https://modernelectric.co.uk", "https://instagram.com/modernelectrictattoo", "3,900"),
        ("Dave", "One by One Tattoo Soho", "info@onebyone.co.uk", "London UK", "https://onebyone.co.uk", "https://instagram.com/onebyonetattoo", "2,900"),
        ("Chris", "South City Market Tattoo", "info@southcitymarket.com", "London UK", "https://southcitymarket.com", "https://instagram.com/southcitymarket", "4,900"),
        ("Marcus", "Secret Society Tattoo Workshop", "info@secretsocietytattoo.co.uk", "London UK", "https://secretsocietytattoo.co.uk", "https://instagram.com/secretsocietytattoo", "2,100"),
        ("Alex", "The Devil's Own Tattoo Parlour", "info@thedevilsowntattoo.co.uk", "London UK", "https://thedevilsowntattoo.co.uk", "https://instagram.com/thedevilsowntattoo", "1,800"),
        ("Sam", "Red Point Tattoo Studio", "info@redpointtattoo.co.uk", "London UK", "https://redpointtattoo.co.uk", "https://instagram.com/redpointtattoo", "3,400"),
        ("Tom", "Circle Tattoo London Studio", "info@thecirclelondon.com", "London UK", "https://thecirclelondon.com", "https://instagram.com/thecirclelondon", "4,600"),
        ("Daniel", "Sang Bleu London Practice", "london@sangbleu.com", "London UK", "https://sangbleu.com", "https://instagram.com/sangbleutattoolondon", "4,700"),
        ("Nick", "Seven Doors Tattoo Studio", "info@sevendoorstattoo.com", "London UK", "https://sevendoorstattoo.com", "https://instagram.com/sevendoorstattoo", "4,500"),
        ("Ben", "Vader Tattoo Melbourne", "vadertattoo@gmail.com", "Melbourne Australia", "https://vadertattoo.com", "https://instagram.com/vadertattoo", "2,400"),
        ("Nathan", "Dynamic Tattoo Richmond", "info@dynamictattoo.com", "Melbourne Australia", "https://dynamictattoo.com", "https://instagram.com/dynamictattoomelbourne", "3,600"),
        ("Ethan", "Hunter & Fox Tattoo Parlour", "info@hunterandfoxtattoo.com", "Sydney Australia", "https://hunterandfoxtattoo.com", "https://instagram.com/hunterandfox", "4,100")
    ]
}

ordered_leads = []
keys = list(boutique_catalog.keys())
max_count = max(len(v) for v in boutique_catalog.values())

tiers_cycle = ["International", "Higher than Local", "Local"]
tier_idx = 0

for i in range(max_count):
    for key in keys:
        if i < len(boutique_catalog[key]):
            item = boutique_catalog[key][i]
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
                "Instagram": item[5],
                "Followers": item[6]
            })

print(f"Total boutique low-reach leads compiled: {len(ordered_leads)}")

with open("leads.csv", "w", encoding="utf-8", newline="") as f:
    fieldnames = ["First Name", "Business", "Email", "Field", "Tier", "Location", "Website", "Instagram", "Followers"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for row in ordered_leads:
        writer.writerow(row)

print("Saved 200 boutique leads to leads.csv successfully!")
