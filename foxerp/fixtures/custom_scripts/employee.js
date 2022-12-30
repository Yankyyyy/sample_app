frappe.ui.form.on('Employee', {
    get_lon_lat(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        if (row.country && (row.city || row.postal_code)){
            var url_link = 'https://nominatim.openstreetmap.org/search.php?country='+ row.country
            if(row.city){
                url_link = url_link + '&city=' + row.city
            }
            if(row.postal_code){
                url_link = url_link + '&postalcode=' + row.postal_code
            }
            url_link = url_link + '&polygon_geojson=1&format=jsonv2'
            
            $.ajax({
                "url": url_link,
                "method": "GET",
                "timeout": 0,
            }).done(function (response) {
                if (response.length != 0){
                    frappe.model.set_value(cdt, cdn, "latitude", response[0].lat);
                    frappe.model.set_value(cdt, cdn, "longitude", response[0].lon);
                }
                else{
                    frappe.model.set_value(cdt, cdn, "latitude", 0);
                    frappe.model.set_value(cdt, cdn, "longitude", 0);
                }
            });
        }
        else{
            frappe.model.set_value(cdt, cdn, "latitude", 0);
            frappe.model.set_value(cdt, cdn, "longitude", 0);
        }
    }
});

frappe.ui.form.on('Employee Geolocation', {
    geolocation(frm, cdt, cdn) {
        let field = locals[cdt][cdn];
        let mapdata =
            JSON.parse(field.geolocation).features[0];
        if (mapdata && mapdata.geometry.type == 'Point') {
            let lat = mapdata.geometry.coordinates[1];
            let lon = mapdata.geometry.coordinates[0];
            field.latitude = lat;
            field.longitude = lon;
            frm.refresh_field('geolocation');
        }
    },
    country(frm, cdt, cdn) {
        frm.events.get_lon_lat(frm, cdt, cdn);
    },
    city(frm, cdt, cdn) {
        frm.events.get_lon_lat(frm, cdt, cdn);
    },
    postal_code(frm, cdt, cdn) {
        frm.events.get_lon_lat(frm, cdt, cdn);
    }
});