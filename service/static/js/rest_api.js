$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#inventory_id").val(res.id);
        $("#inventory_name").val(res.name);
        $("#inventory_condition").val(res.condition);
        $("#inventory_quantity").val(res.quantity);
        $("#inventory_restock_level").val(res.restock_level);
        $("#inventory_created_at").val(res.created_at);
        $("#inventory_updated_at").val(res.updated_at);
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#inventory_id").val("");
        $("#inventory_name").val("");
        $("#inventory_condition").val("");
        $("#inventory_quantity").val("");
        $("#inventory_restock_level").val("");
        $("#inventory_created_at").val("");
        $("#inventory_updated_at").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create an Item
    // ****************************************

    $("#create-btn").click(function () {

        let name = $("#inventory_name").val();
        let condition = $("#inventory_condition").val();
        let quantity = $("#inventory_quantity").val();
        let restock_level = $("#inventory_restock_level").val();

        // Convert input type
        if (!isNaN(quantity)) {
            quantity = parseInt(quantity);
        }
        if (!isNaN(restock_level)) {
            restock_level = parseInt(restock_level);
        }

        let data = {
            "name": name,
            "condition": condition,
            "quantity": quantity,
            "restock_level": restock_level
        };

        $("#flash_message").empty();
        
        let ajax = $.ajax({
            type: "POST",
            url: "/api/inventory",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });

    // ****************************************
    // Restock an Inventory Item
    // ****************************************

    $("#restock-btn").click(function () {
        let id = $("#inventory_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "PUT",
            url: "/api/inventory/".concat(id, "/restock"),
        });

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete an Inventory Item
    // ****************************************

    $("#delete-btn").click(function () {

        let inventory_id = $("#inventory_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "DELETE",
            url: `/api/inventory/${inventory_id}`,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Item has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Retrieve an Inventory Item
    // ****************************************

    $("#retrieve-btn").click(function () {

        let inventory_id = $("#inventory_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/api/inventory/${inventory_id}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Update an Inventory Item
    // ****************************************

    $("#update-btn").click(function () {

        let inventory_id = $("#inventory_id").val();
        let name = $("#inventory_name").val();
        let condition = $("#inventory_condition").val();
        let quantity = $("#inventory_quantity").val();
        let restock_level = $("#inventory_restock_level").val();

        // Convert input type
        if (!isNaN(quantity)) {
            quantity = parseInt(quantity);
        }
        if (!isNaN(restock_level)) {
            restock_level = parseInt(restock_level);
        }

        let data = {
            "name": name,
            "condition": condition,
            "quantity": quantity,
            "restock_level": restock_level
        };

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "PUT",
            url: `/api/inventory/${inventory_id}`,
            contentType: "application/json",
            data: JSON.stringify(data)
        })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Search for an Inventory Item
    // ****************************************

    $("#search-btn").click(function () {

        let name = $("#inventory_name").val();
        let condition = $("#inventory_condition").val();
        let quantity = $("#inventory_quantity").val();
        let restock = $("#inventory_restock_level").val();

        $("#flash_message").empty();

        let queryString = "";

        if (name){
            queryString += "name=" + name
        }
        if (condition){
            if (queryString.length > 0){
                queryString += "&condition=" + condition
            }else{
                queryString += "condition=" + condition
            }
        }

        if (quantity){
            if (queryString.length > 0){
                queryString += "&quantity=" + quantity
            }else{
                queryString += "quantity=" + quantity
            }
        }

        if (restock){
            if (queryString.length > 0){
                queryString += "&restock=" + restock
            }else{
                queryString += "restock=" + restock
            }
        }

        let ajax = $.ajax({
            type: "GET",
            url: `/api/inventory?${queryString}`,
            contentType: "application/json",
            data: ''
        })

        
        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">'
            table += '<thead><tr>'
            table += '<th class="col-md-2">ID</th>'
            table += '<th class="col-md-2">Name</th>'
            table += '<th class="col-md-2">Condition</th>'
            table += '<th class="col-md-2">Quantity</th>'
            table += '<th class="col-md-2">Restock Level</th>'
            table += '</tr></thead><tbody>'
            let firstItem = "";
            for(let i = 0; i < res.length; i++) {
                let item = res[i];
                table +=  `<tr id="row_${i}"><td>${item.id}</td><td>${item.name}</td><td>${item.condition}</td><td>${item.quantity}</td><td>${item.restock_level}</td></tr>`;
                if (i == 0) {
                    firstItem = item;
                }
            }
            table += '</tbody></table>';
            $("#search_results").append(table);

            // copy the first result to the form
            if (firstItem != "") {
                update_form_data(firstItem)
                flash_message("Success")
            }else{
                flash_message("No items found")
            }
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
        
    });

    // ****************************************
    // Clear the form
    // ****************************************
    
    $("#clear-btn").click(function () {
        $("#flash_message").empty();
        clear_form_data()
    });
})
