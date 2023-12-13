from plutus.spiders.builtin_spiders import WalmartSpider


def test_walmart_spider_links():
    url = "https://www.walmart.com/cp/food/976759?povid=GlobalNav_rWeb_Grocery_Grocery_ShopAll"
    with open("tests/data/walmart_spider.html", "rb") as f:
        html = f.read()
    spider = WalmartSpider(url=url, html=html)
    target_links = spider.links()["targets"]
    assert len(target_links) == 56
    assert set(target_links) == {
        "https://walmart.com/ip/Great-Value-Holiday-Ugly-Sweater-Cookie-Kit-Mix-17-68-oz/842820334?athcpid=842820334&athpgid=AthenaContentPage_976759&athcgid=null&athznid=ItemCarousel_9294a23f-f8f6-4efd-aeb4-a61c4005a919_items&athieid=v0&athstid=CS020&athguid=0ceCgfB1K8Isud2g1ag3-2IRPgJcmvaG9m5s&athancid=null&athena=true",
        "https://walmart.com/ip/Kit-Kat-Miniatures-Milk-Chocolate-Wafer-Christmas-Candy-Bag-9-6-oz/554081665?athcpid=554081665&athpgid=AthenaContentPage_976759&athcgid=null&athznid=ItemCarousel_2c581e70-62ae-4746-84bb-8340f8316311_items&athieid=v0&athstid=CS020&athguid=0ceCgfB1K8Isud2g1ag3-2IRPgJcmvaG9m5s&athancid=null&athena=true&athbdg=L1600",
        "https://walmart.com/ip/Beef-Choice-Angus-Prime-Rib-Roast-Halves-Boneless-4-0-6-0-lb/2276384452?athcpid=2276384452&athpgid=AthenaContentPage_976759&athcgid=null&athznid=ItemCarousel_54c3af95-d086-472b-8021-af4727e8b55d_items&athieid=v0&athstid=CS020&athguid=0ceCgfB1K8Isud2g1ag3-2IRPgJcmvaG9m5s&athancid=null&athena=true",
        "https://walmart.com/ip/Great-Value-Holiday-Lights-Multi-Color-Dessert-Sprinkles-2-82-oz/619720754?athcpid=619720754&athpgid=AthenaContentPage_976759&athcgid=null&athznid=ItemCarousel_9294a23f-f8f6-4efd-aeb4-a61c4005a919_items&athieid=v0&athstid=CS020&athguid=0ceCgfB1K8Isud2g1ag3-2IRPgJcmvaG9m5s&athancid=null&athena=true",
        "https://walmart.com/ip/Freshness-Guaranteed-Variety-Cheesecake-16-oz-8-Count/1707826714?athcpid=1707826714&athpgid=AthenaContentPage_976759&athcgid=null&athznid=ItemCarousel_54c3af95-d086-472b-8021-af4727e8b55d_items&athieid=v0&athstid=CS020&athguid=0ceCgfB1K8Isud2g1ag3-2IRPgJcmvaG9m5s&athancid=null&athena=true&athbdg=L1600",
        "https://walmart.com/ip/Bush-s-Original-Baked-Beans-Canned-Beans-28-oz-Can/10306771?athcpid=10306771&athpgid=AthenaContentPage_976759&athcgid=null&athznid=ItemCarousel_9294a23f-f8f6-4efd-aeb4-a61c4005a919_items&athieid=v0&athstid=CS020&athguid=0ceCgfB1K8Isud2g1ag3-2IRPgJcmvaG9m5s&athancid=null&athena=true&athbdg=L1600",
        "https://walmart.com/ip/Ferrero-Rocher-Premium-Milk-Chocolate-Hazelnut-Luxury-Chocolate-Holiday-Gift-16-Count/46000237?athcpid=46000237&athpgid=AthenaContentPage_976759&athcgid=null&athznid=ItemCarousel_2c581e70-62ae-4746-84bb-8340f8316311_items&athieid=v0&athstid=CS020&athguid=0ceCgfB1K8Isud2g1ag3-2IRPgJcmvaG9m5s&athancid=null&athena=true",
        "https://walmart.com/ip/Freshness-Guaranteed-Gingerbread-Ornament-Cookie-Kit-17-6-oz-7-Count/1351073513?athcpid=1351073513&athpgid=AthenaContentPage_976759&athcgid=null&athznid=ItemCarousel_840b81ed-c67f-4fbc-a5d2-6c43722436c8_items&athieid=v0&athstid=CS020&athguid=0ceCgfB1K8Isud2g1ag3-2IRPgJcmvaG9m5s&athancid=null&athena=true",
        "https://walmart.com/ip/Hershey-s-Kisses-Milk-Chocolate-Santa-Hat-Christmas-Candy-Bag-10-1-oz/282587808?athcpid=282587808&athpgid=AthenaContentPage_976759&athcgid=null&athznid=ItemCarousel_2c581e70-62ae-4746-84bb-8340f8316311_items&athieid=v0&athstid=CS020&athguid=0ceCgfB1K8Isud2g1ag3-2IRPgJcmvaG9m5s&athancid=null&athena=true&athbdg=L1600",
        "https://walmart.com/ip/Reese-s-Miniatures-Milk-Chocolate-Peanut-Butter-Cups-Christmas-Candy-Bag-9-9-oz/224508419?athcpid=224508419&athpgid=AthenaContentPage_976759&athcgid=null&athznid=ItemCarousel_2c581e70-62ae-4746-84bb-8340f8316311_items&athieid=v0&athstid=CS020&athguid=0ceCgfB1K8Isud2g1ag3-2IRPgJcmvaG9m5s&athancid=null&athena=true&athbdg=L1600",
        "https://walmart.com/ip/King-s-Hawaiian-Savory-Butter-Rolls-12-Count-12-oz/10421746?athcpid=10421746&athpgid=AthenaContentPage_976759&athcgid=null&athznid=ItemCarousel_54c3af95-d086-472b-8021-af4727e8b55d_items&athieid=v0&athstid=CS020&athguid=0ceCgfB1K8Isud2g1ag3-2IRPgJcmvaG9m5s&athancid=null&athena=true",
        "https://walmart.com/ip/Lindt-Lindor-Assorted-Chocolate-Candy-Truffles-8-5-oz-Bag/46457467?athcpid=46457467&athpgid=AthenaContentPage_976759&athcgid=null&athznid=ItemCarousel_2c581e70-62ae-4746-84bb-8340f8316311_items&athieid=v0&athstid=CS020&athguid=0ceCgfB1K8Isud2g1ag3-2IRPgJcmvaG9m5s&athancid=null&athena=true",
        "https://walmart.com/ip/Freshness-Guaranteed-Assorted-Christmas-Cookies-21-oz-45-Count/657735451?athcpid=657735451&athpgid=AthenaContentPage_976759&athcgid=null&athznid=ItemCarousel_840b81ed-c67f-4fbc-a5d2-6c43722436c8_items&athieid=v0&athstid=CS020&athguid=0ceCgfB1K8Isud2g1ag3-2IRPgJcmvaG9m5s&athancid=null&athena=true",
        "https://walmart.com/ip/Manischewitz-Matzo-Ball-Mix-5-oz/15603544?athcpid=15603544&athpgid=AthenaContentPage_976759&athcgid=null&athznid=ItemCarousel_67b3e558-6d9d-4d15-aba9-a5d08fc2fc71_items&athieid=v0&athstid=CS020&athguid=0ceCgfB1K8Isud2g1ag3-2IRPgJcmvaG9m5s&athancid=null&athena=true&athbdg=L1600",
        "https://walmart.com/ip/Starbucks-Peppermint-Mocha-Frappuccino-12-pack-13-7oz/1797031858?athcpid=1797031858&athpgid=AthenaContentPage_976759&athcgid=null&athznid=ItemCarousel_9294a23f-f8f6-4efd-aeb4-a61c4005a919_items&athieid=v0&athstid=CS020&athguid=0ceCgfB1K8Isud2g1ag3-2IRPgJcmvaG9m5s&athancid=null&athena=true",
        "https://walmart.com/ip/Ferrero-Rocher-Premium-Milk-Chocolate-Hazelnut-Luxury-Chocolate-Holiday-Gift-12-Count/54513665?athcpid=54513665&athpgid=AthenaContentPage_976759&athcgid=null&athznid=ItemCarousel_2c581e70-62ae-4746-84bb-8340f8316311_items&athieid=v0&athstid=CS020&athguid=0ceCgfB1K8Isud2g1ag3-2IRPgJcmvaG9m5s&athancid=null&athena=true&athbdg=L1600",
        "https://walmart.com/ip/Reese-s-Milk-Chocolate-Peanut-Butter-Snack-Size-Trees-Christmas-Candy-Bag-9-6-oz/707917491?athcpid=707917491&athpgid=AthenaContentPage_976759&athcgid=null&athznid=ItemCarousel_2c581e70-62ae-4746-84bb-8340f8316311_items&athieid=v0&athstid=CS020&athguid=0ceCgfB1K8Isud2g1ag3-2IRPgJcmvaG9m5s&athancid=null&athena=true&athbdg=L1600",
        "https://walmart.com/ip/Cinnamon-Croissants-Buns-Breakfast-Pastry-Approx-20-Rugelach-Pastries-No-Coloring-Added-Dairy-Nut-Free-Stern-s-Bakery-Club-Size-19-oz/111468919?athcpid=111468919&athpgid=AthenaContentPage_976759&athcgid=null&athznid=ItemCarousel_67b3e558-6d9d-4d15-aba9-a5d08fc2fc71_items&athieid=v0&athstid=CS020&athguid=0ceCgfB1K8Isud2g1ag3-2IRPgJcmvaG9m5s&athancid=null&athena=true",
        "https://walmart.com/ip/Queen-Anne-Christmas-Milk-Chocolate-Cordial-Cherries-26-4-oz-Box-40-Pieces/21280836?athcpid=21280836&athpgid=AthenaContentPage_976759&athcgid=null&athznid=ItemCarousel_2c581e70-62ae-4746-84bb-8340f8316311_items&athieid=v0&athstid=CS020&athguid=0ceCgfB1K8Isud2g1ag3-2IRPgJcmvaG9m5s&athancid=null&athena=true",
        "https://walmart.com/ip/Great-Value-Fully-Cooked-Italian-Style-Meatballs-32-oz-Frozen/14711314?athcpid=14711314&athpgid=AthenaContentPage_976759&athcgid=null&athznid=ItemCarousel_54c3af95-d086-472b-8021-af4727e8b55d_items&athieid=v0&athstid=CS020&athguid=0ceCgfB1K8Isud2g1ag3-2IRPgJcmvaG9m5s&athancid=null&athena=true&athbdg=L1600",
        "https://walmart.com/ip/Manischewitz-Hometstyle-Medium-Egg-Noodles-12oz/1670215763?athcpid=1670215763&athpgid=AthenaContentPage_976759&athcgid=null&athznid=ItemCarousel_67b3e558-6d9d-4d15-aba9-a5d08fc2fc71_items&athieid=v0&athstid=CS020&athguid=0ceCgfB1K8Isud2g1ag3-2IRPgJcmvaG9m5s&athancid=null&athena=true",
        "https://walmart.com/ip/M-M-s-Holiday-Peanut-Milk-Chocolate-Christmas-Candy-10-oz-Bag/312693860?athcpid=312693860&athpgid=AthenaContentPage_976759&athcgid=null&athznid=ItemCarousel_2c581e70-62ae-4746-84bb-8340f8316311_items&athieid=v0&athstid=CS020&athguid=0ceCgfB1K8Isud2g1ag3-2IRPgJcmvaG9m5s&athancid=null&athena=true&athbdg=L1600",
        "https://walmart.com/ip/Queen-Anne-Milk-Chocolate-Cordial-Cherries-6-6-oz-Box-10-Pieces/28131212?athcpid=28131212&athpgid=AthenaContentPage_976759&athcgid=null&athznid=ItemCarousel_2c581e70-62ae-4746-84bb-8340f8316311_items&athieid=v0&athstid=CS020&athguid=0ceCgfB1K8Isud2g1ag3-2IRPgJcmvaG9m5s&athancid=null&athena=true&athbdg=L1600",
        "https://walmart.com/ip/Freshness-Guaranteed-Mini-Deck-the-Halls-Frosted-Sugar-Cookies-9-4-oz-18-Count/1444729853?athcpid=1444729853&athpgid=AthenaContentPage_976759&athcgid=null&athznid=ItemCarousel_840b81ed-c67f-4fbc-a5d2-6c43722436c8_items&athieid=v0&athstid=CS020&athguid=0ceCgfB1K8Isud2g1ag3-2IRPgJcmvaG9m5s&athancid=null&athena=true",
        "https://walmart.com/ip/Terry-s-Chocolate-Orange-Orange-Flavored-Original-Milk-Chocolate-Confection-5-53oz-Box/263035009?athcpid=263035009&athpgid=AthenaContentPage_976759&athcgid=null&athznid=ItemCarousel_2c581e70-62ae-4746-84bb-8340f8316311_items&athieid=v0&athstid=CS020&athguid=0ceCgfB1K8Isud2g1ag3-2IRPgJcmvaG9m5s&athancid=null&athena=true&athbdg=L1600",
        "https://walmart.com/ip/Beef-Choice-Angus-Chuck-Roast-2-00-2-75-lb-Tray/39944474?athcpid=39944474&athpgid=AthenaContentPage_976759&athcgid=null&athznid=ItemCarousel_54c3af95-d086-472b-8021-af4727e8b55d_items&athieid=v0&athstid=CS020&athguid=0ceCgfB1K8Isud2g1ag3-2IRPgJcmvaG9m5s&athancid=null&athena=true&athbdg=L1600",
        "https://walmart.com/ip/Sam-s-Choice-Cooked-Medium-Shrimp-Cocktail-Ring-with-Sauce-16-oz/949906404?athcpid=949906404&athpgid=AthenaContentPage_976759&athcgid=null&athznid=ItemCarousel_54c3af95-d086-472b-8021-af4727e8b55d_items&athieid=v0&athstid=CS020&athguid=0ceCgfB1K8Isud2g1ag3-2IRPgJcmvaG9m5s&athancid=null&athena=true",
        "https://walmart.com/ip/Freshness-Guaranteed-Frosted-Sugar-Cookies-13-5-oz-10-Count/163566200?athcpid=163566200&athpgid=AthenaContentPage_976759&athcgid=null&athznid=ItemCarousel_840b81ed-c67f-4fbc-a5d2-6c43722436c8_items&athieid=v0&athstid=CS020&athguid=0ceCgfB1K8Isud2g1ag3-2IRPgJcmvaG9m5s&athancid=null&athena=true",
        "https://walmart.com/ip/Lindt-LINDOR-Holiday-Milk-Chocolate-Candy-Truffles-8-5-oz-Bag/46457465?athcpid=46457465&athpgid=AthenaContentPage_976759&athcgid=null&athznid=ItemCarousel_2c581e70-62ae-4746-84bb-8340f8316311_items&athieid=v0&athstid=CS020&athguid=0ceCgfB1K8Isud2g1ag3-2IRPgJcmvaG9m5s&athancid=null&athena=true",
        "https://walmart.com/ip/M-M-s-Milk-Chocolate-Christmas-Candy-10-oz-Bag/321933875?athcpid=321933875&athpgid=AthenaContentPage_976759&athcgid=null&athznid=ItemCarousel_2c581e70-62ae-4746-84bb-8340f8316311_items&athieid=v0&athstid=CS020&athguid=0ceCgfB1K8Isud2g1ag3-2IRPgJcmvaG9m5s&athancid=null&athena=true&athbdg=L1600",
        "https://walmart.com/ip/Freshness-Guaranteed-Christmas-Gingerbread-House-Kit-35-3-oz-1-Count/1195792225?athcpid=1195792225&athpgid=AthenaContentPage_976759&athcgid=null&athznid=ItemCarousel_840b81ed-c67f-4fbc-a5d2-6c43722436c8_items&athieid=v0&athstid=CS020&athguid=0ceCgfB1K8Isud2g1ag3-2IRPgJcmvaG9m5s&athancid=null&athena=true&athbdg=L1600",
        "https://walmart.com/ip/Queen-Anne-Dark-Chocolate-Cordial-Cherries-6-6-oz-Box-10-Pieces/28131215?athcpid=28131215&athpgid=AthenaContentPage_976759&athcgid=null&athznid=ItemCarousel_2c581e70-62ae-4746-84bb-8340f8316311_items&athieid=v0&athstid=CS020&athguid=0ceCgfB1K8Isud2g1ag3-2IRPgJcmvaG9m5s&athancid=null&athena=true&athbdg=L1600",
        "https://walmart.com/ip/Do-It-Yourself-Chanukah-House-Cookie-Decorating-Kit-By-Manischewitz-Easy-Build-Tray-Included-Nut-Free-Fun-Hanukkah-Activity-for-the-Whole-Family/799789065?athcpid=799789065&athpgid=AthenaContentPage_976759&athcgid=null&athznid=ItemCarousel_67b3e558-6d9d-4d15-aba9-a5d08fc2fc71_items&athieid=v0&athstid=CS020&athguid=0ceCgfB1K8Isud2g1ag3-2IRPgJcmvaG9m5s&athancid=null&athena=true",
        "https://walmart.com/ip/Hershey-s-Kisses-Milk-Chocolate-Christmas-Candy-Bag-10-1-oz/280164233?athcpid=280164233&athpgid=AthenaContentPage_976759&athcgid=null&athznid=ItemCarousel_54c3af95-d086-472b-8021-af4727e8b55d_items&athieid=v0&athstid=CS020&athguid=0ceCgfB1K8Isud2g1ag3-2IRPgJcmvaG9m5s&athancid=null&athena=true&athbdg=L1600",
        "https://walmart.com/ip/York-Dark-Chocolate-Peppermint-Patties-Snowflakes-Christmas-Candy-Bag-9-6-oz/700609733?athcpid=700609733&athpgid=AthenaContentPage_976759&athcgid=null&athznid=ItemCarousel_2c581e70-62ae-4746-84bb-8340f8316311_items&athieid=v0&athstid=CS020&athguid=0ceCgfB1K8Isud2g1ag3-2IRPgJcmvaG9m5s&athancid=null&athena=true&athbdg=L1600",
        "https://walmart.com/ip/Little-Debbie-Vanilla-Christmas-Tree-Cakes-8-52-oz-5-Count/19757433?athcpid=19757433&athpgid=AthenaContentPage_976759&athcgid=null&athznid=ItemCarousel_9294a23f-f8f6-4efd-aeb4-a61c4005a919_items&athieid=v0&athstid=CS020&athguid=0ceCgfB1K8Isud2g1ag3-2IRPgJcmvaG9m5s&athancid=null&athena=true&athbdg=L1600",
        "https://walmart.com/ip/Rotel-Mild-Diced-Tomatoes-and-Green-Chilies-10-oz/10308582?athcpid=10308582&athpgid=AthenaContentPage_976759&athcgid=null&athznid=ItemCarousel_9294a23f-f8f6-4efd-aeb4-a61c4005a919_items&athieid=v0&athstid=CS020&athguid=0ceCgfB1K8Isud2g1ag3-2IRPgJcmvaG9m5s&athancid=null&athena=true&athbdg=L1600",
        "https://walmart.com/ip/Manischewitz-Matzo-Balls-In-Broth-24-oz-4-pack/1364679540?athcpid=1364679540&athpgid=AthenaContentPage_976759&athcgid=null&athznid=ItemCarousel_67b3e558-6d9d-4d15-aba9-a5d08fc2fc71_items&athieid=v0&athstid=CS020&athguid=0ceCgfB1K8Isud2g1ag3-2IRPgJcmvaG9m5s&athancid=null&athena=true",
        "https://walmart.com/ip/Welch-s-Non-Alcoholic-Sparkling-100-Apple-Juice-Cider-25-4-fl-oz-Bottle/545161771?athcpid=545161771&athpgid=AthenaContentPage_976759&athcgid=null&athznid=ItemCarousel_54c3af95-d086-472b-8021-af4727e8b55d_items&athieid=v0&athstid=CS020&athguid=0ceCgfB1K8Isud2g1ag3-2IRPgJcmvaG9m5s&athancid=null&athena=true",
        "https://walmart.com/ip/GHIRARDELLI-Peppermint-Bark-Chocolate-Squares-7-9-oz-Bag/46089049?athcpid=46089049&athpgid=AthenaContentPage_976759&athcgid=null&athznid=ItemCarousel_2c581e70-62ae-4746-84bb-8340f8316311_items&athieid=v0&athstid=CS020&athguid=0ceCgfB1K8Isud2g1ag3-2IRPgJcmvaG9m5s&athancid=null&athena=true&athbdg=L1600",
        "https://walmart.com/ip/Tabatchnick-Classic-Wholesome-Chicken-Broth-32-Fl-oz-4-pack/1951268592?athcpid=1951268592&athpgid=AthenaContentPage_976759&athcgid=null&athznid=ItemCarousel_67b3e558-6d9d-4d15-aba9-a5d08fc2fc71_items&athieid=v0&athstid=CS020&athguid=0ceCgfB1K8Isud2g1ag3-2IRPgJcmvaG9m5s&athancid=null&athena=true",
        "https://walmart.com/ip/Marketside-Pepperoni-Pizza-Traditional-Crust-Extra-Large-Marinara-Sauce-44-6-oz-Fresh/579824441?athcpid=579824441&athpgid=AthenaContentPage_976759&athcgid=null&athznid=ItemCarousel_9294a23f-f8f6-4efd-aeb4-a61c4005a919_items&athieid=v0&athstid=CS020&athguid=0ceCgfB1K8Isud2g1ag3-2IRPgJcmvaG9m5s&athancid=null&athena=true&athbdg=L1600",
        "https://walmart.com/ip/Sam-s-Choice-Spiral-Cut-Honey-Cured-Double-Glaze-Ham-8-14-6-lb/155067647?athcpid=155067647&athpgid=AthenaContentPage_976759&athcgid=null&athznid=ItemCarousel_54c3af95-d086-472b-8021-af4727e8b55d_items&athieid=v0&athstid=CS020&athguid=0ceCgfB1K8Isud2g1ag3-2IRPgJcmvaG9m5s&athancid=null&athena=true&athbdg=L1600",
        "https://walmart.com/ip/Hershey-s-Kisses-Candy-Cane-Flavored-Christmas-Candy-Bag-9-oz/976682301?athcpid=976682301&athpgid=AthenaContentPage_976759&athcgid=null&athznid=ItemCarousel_2c581e70-62ae-4746-84bb-8340f8316311_items&athieid=v0&athstid=CS020&athguid=0ceCgfB1K8Isud2g1ag3-2IRPgJcmvaG9m5s&athancid=null&athena=true&athbdg=L1600",
        "https://walmart.com/ip/Great-Value-Coffee-Creamer-Peppermint-Bark-32-fl-oz/771348264?athcpid=771348264&athpgid=AthenaContentPage_976759&athcgid=null&athznid=ItemCarousel_9294a23f-f8f6-4efd-aeb4-a61c4005a919_items&athieid=v0&athstid=CS020&athguid=0ceCgfB1K8Isud2g1ag3-2IRPgJcmvaG9m5s&athancid=null&athena=true&athbdg=L1600",
        "https://walmart.com/ip/Nancy-s-Petite-Quiche-Frozen-Snacks-Variety-Pack-32-Ct-Box-Regular/15610919?athcpid=15610919&athpgid=AthenaContentPage_976759&athcgid=null&athznid=ItemCarousel_54c3af95-d086-472b-8021-af4727e8b55d_items&athieid=v0&athstid=CS020&athguid=0ceCgfB1K8Isud2g1ag3-2IRPgJcmvaG9m5s&athancid=null&athena=true",
        "https://walmart.com/ip/Freshness-Guaranteed-Pecan-Divinity-Candy-12-oz/1279910745?athcpid=1279910745&athpgid=AthenaContentPage_976759&athcgid=null&athznid=ItemCarousel_840b81ed-c67f-4fbc-a5d2-6c43722436c8_items&athieid=v0&athstid=CS020&athguid=0ceCgfB1K8Isud2g1ag3-2IRPgJcmvaG9m5s&athancid=null&athena=true",
        "https://walmart.com/ip/Fresh-Hass-Avocados-Each/44390949?athcpid=44390949&athpgid=AthenaContentPage_976759&athcgid=null&athznid=ItemCarousel_9294a23f-f8f6-4efd-aeb4-a61c4005a919_items&athieid=v0&athstid=CS020&athguid=0ceCgfB1K8Isud2g1ag3-2IRPgJcmvaG9m5s&athancid=null&athena=true&athbdg=L1600",
        "https://walmart.com/ip/Smirnoff-Ice-Red-White-Berry-Sparkling-Drink-11-2oz-Bottles-6pk/941741487?athcpid=941741487&athpgid=AthenaContentPage_976759&athcgid=null&athznid=ItemCarousel_9294a23f-f8f6-4efd-aeb4-a61c4005a919_items&athieid=v0&athstid=CS020&athguid=0ceCgfB1K8Isud2g1ag3-2IRPgJcmvaG9m5s&athancid=null&athena=true",
        "https://walmart.com/ip/Freshness-Guaranteed-Holiday-Brownie-Bites-22-2-oz-33-Count-Sweet-Dessert/152711745?athcpid=152711745&athpgid=AthenaContentPage_976759&athcgid=null&athznid=ItemCarousel_840b81ed-c67f-4fbc-a5d2-6c43722436c8_items&athieid=v0&athstid=CS020&athguid=0ceCgfB1K8Isud2g1ag3-2IRPgJcmvaG9m5s&athancid=null&athena=true",
        "https://walmart.com/ip/Snickers-Minis-Milk-Chocolate-Christmas-Candy-Bars-10-48-Oz-Bag/384633778?athcpid=384633778&athpgid=AthenaContentPage_976759&athcgid=null&athznid=ItemCarousel_2c581e70-62ae-4746-84bb-8340f8316311_items&athieid=v0&athstid=CS020&athguid=0ceCgfB1K8Isud2g1ag3-2IRPgJcmvaG9m5s&athancid=null&athena=true&athbdg=L1600",
        "https://walmart.com/ip/Toasteds-Variety-Pack-Crackers-12-oz/11045794?athcpid=11045794&athpgid=AthenaContentPage_976759&athcgid=null&athznid=ItemCarousel_54c3af95-d086-472b-8021-af4727e8b55d_items&athieid=v0&athstid=CS020&athguid=0ceCgfB1K8Isud2g1ag3-2IRPgJcmvaG9m5s&athancid=null&athena=true&athbdg=L1600",
        "https://walmart.com/ip/Hillshire-Farm-Lit-l-Smokies-Smoked-Sausage-28-oz/44391041?athcpid=44391041&athpgid=AthenaContentPage_976759&athcgid=null&athznid=ItemCarousel_9294a23f-f8f6-4efd-aeb4-a61c4005a919_items&athieid=v0&athstid=CS020&athguid=0ceCgfB1K8Isud2g1ag3-2IRPgJcmvaG9m5s&athancid=null&athena=true&athbdg=L1600",
        "https://walmart.com/ip/Fancy-Sprinkles-Jingle-Juice-Cocktail-and-Mocktail-Holiday-Drink-Decorating-Kit-2-1-oz/2916794145?athcpid=2916794145&athpgid=AthenaContentPage_976759&athcgid=null&athznid=ItemCarousel_54c3af95-d086-472b-8021-af4727e8b55d_items&athieid=v0&athstid=CS020&athguid=0ceCgfB1K8Isud2g1ag3-2IRPgJcmvaG9m5s&athancid=null&athena=true",
        "https://walmart.com/ip/Capri-Sun-Variety-Pack-with-Fruit-Punch-Strawberry-Kiwi-Pacific-Cooler-Juice-Box-Pouches-30-ct-Box-6-fl-oz-Pouches/110946086?athcpid=110946086&athpgid=AthenaContentPage_976759&athcgid=null&athznid=ItemCarousel_9294a23f-f8f6-4efd-aeb4-a61c4005a919_items&athieid=v0&athstid=CS020&athguid=0ceCgfB1K8Isud2g1ag3-2IRPgJcmvaG9m5s&athancid=null&athena=true&athbdg=L1600",
        "https://walmart.com/ip/Little-Debbie-Christmas-Tree-Cake-Ice-Cream-Cake-Chunks-Green-Sprinkles-and-Red-Icing-16-fl-oz/864056546?athcpid=864056546&athpgid=AthenaContentPage_976759&athcgid=null&athznid=ItemCarousel_9294a23f-f8f6-4efd-aeb4-a61c4005a919_items&athieid=v0&athstid=CS020&athguid=0ceCgfB1K8Isud2g1ag3-2IRPgJcmvaG9m5s&athancid=null&athena=true&athbdg=L1600",
    }
    spiderable_links = spider.links()["spiderables"]
    assert len(spiderable_links) == 25
    assert set(spiderable_links) == {
        "https://walmart.com/cp/bakery-bread/976779?povid=976759_hubspoke_976759_Freshfoods_BreadandBakery_Rweb_Aug_18",
        "https://walmart.com/cp/grab-go/3701649?povid=976759_hubspoke_976759_Evenmore_GrabandGo_Rweb_Aug_18",
        "https://walmart.com/cp/meat-seafood/9569500?povid=976759_hubspoke_976759_Freshfoods_MeatandSeafood_Rweb_Aug_18",
        "https://walmart.com/cp/frozen-foods/976791?povid=976759_hubspoke_976759_Stockuponessentials_Frozen_Rweb_Aug_18",
        "https://walmart.com/browse/food/parfaits/976759_1567409_6592518_7031854",
        "https://walmart.com/browse/food/great-value-cookies/976759_976787_1001391_2474028",
        "https://walmart.com/cp/dairy-eggs/9176907?povid=976759_hubspoke_976759_Freshfoods_DairyandEggs_Rweb_Aug_18",
        "https://walmart.com/cp/breakfast-cereal/976783?povid=976759_hubspoke_976759_Stockuponessentials_BreakfastandCereal_Rweb_Aug_18",
        "https://walmart.com/cp/clothing/5438?povid=976759_HubSpoke_7998220_XSell_HolidayFashion_11_03",
        "https://walmart.com/browse/food/fat-free-food/976759_1567409_3170630_8672408",
        "https://walmart.com/cp/fresh-produce/976793?povid=976759_hubspoke_976759_Freshfoods_Produce_Rweb_Aug_18",
        "https://walmart.com/cp/candy-gum/1096070?povid=976759_hubspoke_976759_Evenmore_Candy_Rweb_Aug_18",
        "https://walmart.com/cp/meal-solutions-grains-pasta/976794?povid=976759_hubspoke_976759_Stockuponessentials_Pantry_Rweb_Aug_18",
        "https://walmart.com/cp/snacks-cookies-chips/976787?povid=976759_hubspoke_976759_Stockuponessentials_Snacks_Rweb_Aug_18",
        "https://walmart.com/cp/beverages/976782?povid=976759_hubspoke_976759_Stockuponessentials_Beverages_Rweb_Aug_18",
        "https://walmart.com/cp/christmas-decor/7472650?povid=ApparelNav_WOMENS_Womens_CP_Hubspokes_Cat_EverythingHoliday_Christmasdecor",
        "https://walmart.com/cp/coffee/1086446?povid=976759_hubspoke_976759_Stockuponessentials_Coffee_Rweb_Aug_18",
        "https://walmart.com/browse/all-food/976759_9638107",
        "https://walmart.com/cp/meat-seafood-buying-guide/6677247?povid=976759_hubspoke_976759_Freshfoods_Beefbuyingguide_Rweb_Aug_18",
        "https://walmart.com/cp/from-our-brands/7128585?povid=976759_hubspoke_976759_Evenmore_Ourbrands_Rweb_Aug_18",
        "https://walmart.com/browse/food/sandwich-toppings/976759_1567409_7966149_3796833",
        "https://walmart.com/browse/food/summer-flavors/976759_1567409_3534625_5791075",
        "https://walmart.com/cp/baking/976780?povid=976759_hubspoke_976759_Evenmore_Baking_Rweb_Aug_18",
        "https://walmart.com/cp/seafood-meal-options/3410728?povid=976759_LHNCP_976759_Categories_MeatSeafood_Seafoodbuyingguide_02_10",
        "https://walmart.com/cp/international-food/7404240?povid=976759_hubspoke_976759_Evenmore_Internationalfoods_Rweb_Aug_18",
    }