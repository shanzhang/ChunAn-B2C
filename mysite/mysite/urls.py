from django.conf.urls import patterns, include, url
from django.shortcuts import render_to_response
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^django_admin/', include(admin.site.urls)),
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.STATIC_DOC_ROOT}),

    #market module
    (r'^$','market.views.market'),
    (r'^home$','market.views.market'),
    (r'^market_display$','market.views.market_display'),
    (r'^terms$','market.views.terms'),

    #address module
    (r'^addAddress$','address.views.addAddress'),
    (r'^loadAddressBook$','address.views.loadAddressBook'),
    (r'^modAddress$','address.views.modAddress'),
    (r'^delAddress$','address.views.delAddress'),

    #search_module
    (r'^search$','search.views.search'),
    (r'^searchResult$','search.views.searchResult'),

    #product module
    (r'^detail/pid/(\d+)','product.views.detail_display'),
    (r'^loadCompare$','product.views.loadCompare'),
    (r'^loadNewOn$','product.views.loadNewOn'),

    #category_module
    (r'^category$','category.views.category_display'),
    (r'^category_main$','category.views.category_main'),
    (r'^cid/(\d+)', 'category.views.category_product'),
    (r'^loadAllProduct$','category.views.loadAllProduct'),

    #order_module
    (r'^order$','order.views.order_display'),
    (r'^loadOrder$','order.views.loadOrder'),
    (r'^loadOrderList$','order.views.loadOrderList'),
    (r'^payPass$','order.views.payPass'),
    (r'^pay$','order.views.pay'),
    (r'^receiveProduct$','order.views.receiveProduct'),

    #cart_module
    (r'^cart$','cart.views.cart_display'),
    (r'^addToCart$','cart.views.addToCart'),
    (r'^loadCart$','cart.views.loadCart'),
    (r'^delCart$','cart.views.delCart'),
    (r'^delCartItem/(\d+)','cart.views.delCartItem'),
    (r'^updateCartItem$','cart.views.updateCartItem'),

    #fav_module
    (r'^addToFav/pid/(\d+)','favorites.views.addToFav'),
    (r'^favorites$','favorites.views.favorites'),
    (r'^loadFav$','favorites.views.loadFav'),
    (r'^delFav$','favorites.views.delFav'),
    (r'^delFavItem/(\d+)','favorites.views.delFavItem'),

    #customer module
    (r'^logout$','customer.views.logout'),
    (r'^register$','customer.views.register'),
    (r'^verifyUser$','customer.views.verifyUser'),
    (r'^createUser$','customer.views.createUser'),
    (r'^account$','customer.views.account'),
    (r'^account_admin$','customer.views.account_admin'),
    (r'^changeInfo$','customer.views.changeInfo'),
    (r'^changeInfo_admin$','customer.views.changeInfo_admin'),

    #admin_module
    (r'^admin$','admin.views.admin_display'),
    (r'^add_category$','admin.views.add_category'),
    (r'^del_category$','admin.views.del_category'),
    (r'^mod_category$','admin.views.mod_category'),
    (r'^add_product$','admin.views.add_product'),
    (r'^del_product$','admin.views.del_product'),
    (r'^mod_product$','admin.views.mod_product'),
    (r'^add_groupon$','admin.views.add_groupon'),
    (r'^del_groupon$','admin.views.del_groupon'),
    (r'^mod_groupon$','admin.views.mod_groupon'),
    (r'^addGroupon$','admin.views.addGroupon'),
    (r'^loadCategory$','admin.views.loadCategory'),
    (r'^addCategory$','admin.views.addCategory'),
    (r'^deleteCategory$','admin.views.deleteCategory'),
    (r'^modifyCategory$','admin.views.modifyCategory'),
    (r'^loadLeafCategory$','admin.views.loadLeafCategory'),
    (r'^addProduct$','admin.views.addProduct'),
    (r'^loadProduct$','admin.views.loadProduct'),
    (r'^loadProductInfo$','admin.views.loadProductInfo'),
    (r'^deleteProduct$','admin.views.deleteProduct'),
    (r'^modifyProduct$','admin.views.modifyProduct'),
    (r'^search_product$','admin.views.search_product'),
    (r'^process_order$','admin.views.process_order'),
    (r'^search_order$','admin.views.search_order'),
    (r'^loadOrderAdmin$','admin.views.loadOrderAdmin'),
    (r'^searchOrderAdmin$','admin.views.searchOrderAdmin'),
    (r'^sendProduct$','admin.views.sendProduct'),
    (r'^activateUser$','admin.views.activateUser'),
    (r'^searchUser$','admin.views.searchUser'),
    (r'^manage_user$','admin.views.manageUser'),
    (r'^loadAllOrderAdmin$','admin.views.loadAllOrderAdmin'),
    (r'^dp_groupon$','admin.views.dp_groupon'),
    (r'^add_pure_groupon$','admin.views.add_pure_groupon'),
    (r'^adminUser$','admin.views.adminUser'),
    
    #usr module
    (r'^allUser$','usr.views.allUser'),

    #groupon module
    (r'^groupon$','groupon.views.groupon'),
    (r'^getAllItem$','groupon.views.getAllItem'),
    (r'^payGroupon$','groupon.views.payGroupon'),
    (r'^display_Groupon$','groupon.views.getAllItem'),
    (r'^delay_groupon$','groupon.views.delay_groupon'),

)