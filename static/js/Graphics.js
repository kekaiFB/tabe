//https://datatables.net/blog/2020-10-01
//https://code.tutsplus.com/ru/tutorials/getting-started-with-chartjs-line-and-bar-charts--cms-28384
function chartData(table) {
    var counts = {};

    table.rows({ search: 'applied' }).data().each(function (val) {

        if (counts[val.slice(4,5)]) {
            counts[val.slice(4,5)] += parseInt(val[7]);
        } else {
            counts[val.slice(4,5)] = parseInt(val[7]);
        }
    });

    // And map it to the format highcharts uses
    return $.map(counts, function (val, key) {
        return {
            label: key,
            value: val,
        };
    });
}


function chartDataOffice(table) {
    var counts = {};
 
    // Count the number of entries for each office
    table.rows({ search: 'applied' }).data().each(function (val) {
        if (counts[val[2]]) {
            counts[val[2]] += parseInt(val[7]);
        } else {
            counts[val[2]] = parseInt(val[7]);
        }
    });
 
    // And map it to the format highcharts uses
    return $.map(counts, function (val, key) {
        return {
            label: key,
            value: val,
        };
    });
}




function chartDataDate(table) {
    var startDate = moment('2023-01-01');
    var endDate = moment('2024-01-01');
    var date = [];

    for (var m = moment(startDate); m.isBefore(endDate+1); m.add(1, 'days')) {
        date.push(m.format('YYYY-MM-DD'));
    }

    var counts = {};
    var countsReason = {};
    for (var i = 0; i<date.length; i++) {
        counts[date[i]] = 0;
        countsReason[date[i]] = 0;
    };

    for (var i = 0; i<date.length; i++) {
        table.rows({ search: 'applied' }).data().each(function (val) {
            var thisdate = date[i];
            if (thisdate >= val[8] && thisdate <= val[9]){
                counts[thisdate] += 1; 
            } 
        });

    }    

 
    return $.map(counts, function (val, key) {
       
        return {
            label: key,
            value: val,
        };
    });
}


function month(table, reason) {
    
    var startDate = moment('2023-01-01');
    var endDate = moment('2023-12-31');
    var date = [];

    for (var m = moment(startDate); m.isBefore(endDate+1); m.add(1, 'days')) {
        date.push(m.format('YYYY-MM-DD'));
    }

    var counts = {};
    for (var i = 0; i<date.length; i++) {
        counts[date[i]] = 0;
    };

    for (var i = 0; i<date.length; i++) {
        table.rows({ search: 'applied' }).data().each(function (val) {
            var thisdate = date[i];
            if (val[5] == reason) {
                if (thisdate >= val[8] && thisdate <= val[9]){
                    counts[thisdate] += 1; 
                } 
            }
            
        });

    }
    
   

    return $.map(counts, function (val, key) {
        return {
            label: key.slice(0, -3),
            value: val,
        };
    });
    
}



function chartDataMonth(table, reason = '') {
    var data = month(table, reason);
    var count = {};

    data.map( function( value, key ) {
        var key = value['label']
        var value = value['value']
        
        if (count.hasOwnProperty(key)) {
        } else {
            count[key] = 0;
        }
    });
    data.map( function( value, key ) {
        var key = value['label']
        var value = value['value']
        count[key] += value;
        
    });

    
    var monthNames = [ "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь" ]; 
    

    return $.map(count, function (val, key) {
        key= monthNames[0]
        monthNames.shift() 
        return {
            label: key,
            value: val,
        };
    });
    
}

