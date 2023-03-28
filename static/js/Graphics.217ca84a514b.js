//https://datatables.net/blog/2020-10-01
//https://code.tutsplus.com/ru/tutorials/getting-started-with-chartjs-line-and-bar-charts--cms-28384
function chartData(table, reason='') {
    var counts = {};
    table.rows({ search: 'applied' }).data().each(function (val) {
        if (!counts[val[4]]) {
            counts[val[4]] = 0;
        } 
    });

    table.rows({ search: 'applied' }).data().each(function (val) {
        if (reason != ''){
            if (val[5] == reason) {
                counts[val[4]] += parseInt(val[7]);
            }
        }
    });

    return $.map(counts, function (val, key) {
        return {
            label: key,
            value: val,
        };
    });
}


function chartDataOffice(table) {
    var counts = {};
    var human;
    human = table.column(4).data().unique().toArray();

    //находим уникальных сотрундников, их офис, и считаем повторения такого офиса
    table.rows({ search: 'applied' }).data().each(function (val) {
        if ( human.includes(val[4]))
        {
            if (counts[val[2]]) {
                counts[val[2]] += 1;
            } else {
                counts[val[2]] = 1;
            }
           human = human.filter(function(f) { return f !== val[4] })
        };   
    });

    return $.map(counts, function (val, key) {
        return {
            label: key,
            value: val,
        };
    });
}
 



function chartDataDate(table) {
    var startDate = moment().subtract(0, 'year').startOf('year').format('YYYY-MM-DD');
    var endDate = moment().subtract(-1, 'year').startOf('year').format('YYYY-MM-DD');
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
    var startDate = moment().subtract(0, 'year').startOf('year').format('YYYY-MM-DD');
    var endDate = moment().subtract(0, 'year').endOf('year').format('YYYY-MM-DD')

    var date = [];

    for (var m = moment(startDate); m.isBefore(endDate); m.add(1, 'days')) {
        date.push(m.format('YYYY-MM-DD'));
    }

    var counts = {};
    for (var i = 0; i<date.length; i++) {
        counts[date[i]] = 0;
    };

    for (var i = 0; i<date.length; i++) {
        table.rows({ search: 'applied' }).data().each(function (val) {
            var thisdate = date[i];
            if (reason != '') {
                if (val[5] == reason) {
                    if (thisdate >= val[8] && thisdate <= val[9]){
                        counts[thisdate] += 1; 
                    } 
                }
            } else {
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


var rgbaColor;

//рандомненое число для rgb
function colorGen () { 
  var generateColor = Math.floor(Math.random() * 256 );
  return generateColor;
}



//датасет для графика
function getDataset(title, data) {
  rgbaColor = 'rgba(' + colorGen() + ',' + colorGen() + ',' + colorGen() + ', ';
  return { 
    label: title + '. Пропуски',
    data: data,
    backgroundColor: rgbaColor + ' 0.2)',
    borderColor: rgbaColor + ' 1)',
    borderWidth: 1, 
  }; 
}

function reasonGraphicMonth(table) {
    var datasets = []
    var value;

    //ищем все причины пропуска работы
    var reason =  table
    .column(5)
    .data()
    .unique();
    
    //ищем для каждой причины количество пропусков и добавляем в датасет
    reason.map( function(reas) {
        value = chartDataMonth(table, reas).map( function( value ) {
            return value['value']
        }) 
        datasets.push(getDataset(reas, value));     
    });

    return datasets
}



function reasonGraphicHuman(table) {
    var datasets = []
    var value;

    //ищем все причины пропуска работы
    var reason =  table
    .column(5)
    .data()
    .unique();
    
    //ищем для каждой причины количество пропусков по сотруднику и добавляем в датасет
    reason.map( function(reas) {
        value = chartData(table, reas).map( function( value ) {
            return value['value']
        }) 
        datasets.push(getDataset(reas, value));     
    });
    return datasets
}

function addMonthOfDay(elem) {
    var monthNames = [ "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь" ]; 
    var month= new Date(elem).getMonth();
    return elem + ';' + monthNames[month]
}

function getMonthOfDayArray(array) {
    return array.map(addMonthOfDay);   
}
