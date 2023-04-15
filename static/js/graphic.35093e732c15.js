var myChart1;
var labels_tgo=[], time_start=[], time_end=[]; 
const ctx1 = document.getElementById('oneChart').getContext('2d');


function draw_tgo_table (table) {

    //ПЕРВЫЙ ГРАФИК
    var length = table.getColumnData([0]).length


    //ПОДГОТОВКА ДАННЫХ
    var e = 'E'
    var f = 'F'

    for (let i = 0; i < length; i++) { 
        res = table.getRowData(i);
        time_start.push(table.getLabel(e + i))
        time_end.push(table.getLabel(f + i))
        labels_tgo.push(res[0])
    }

    //удаляем ненужные данные
    time_start.shift()
    time_end.shift()
    labels_tgo.pop(0)
   // labels_tgo.reverse()


    //приводим данные к читабельному виду для chart.js
    time_start = time_start.map(function(x){ return x.slice(0, -3) });
    time_end = time_end.map(function(x){ return x.slice(0, -3) });

    //для x: stacke=true
    time_end = time_end.map(function(val, i) {
        return time_end[i] - time_start[i]
      })

    init();

    
}

function init() {

    //ПЕРВЫЙ ГРАФИК
    myChart1 = new Chart(ctx1, {
        type: 'bar',
        data: {
            labels: labels_tgo,
            datasets: [{
                label: 'начало(мин.)',
                data: time_start,
              //  backgroundColor: 'rbga(255,255,255, 0.1)',
            },
            {
                label: 'длительность(мин.)',
                data: time_end,
                backgroundColor: 'rgba(220,20,60, 0.8)'
            },
            
            ],
          },   
        options: {
            indexAxis: 'y',
            elements: {
                bar: {
                    borderWidth: 2,
                }
            },
            plugins: {
                enabled: false,
                legend: {
                    position: 'right',
                },
                title: {
                    display: true,
                    text: 'Технологический график обслуживания'
                }
            },

            scales: {
            
                    x: {      
                        stacked: true,
                        beginAtZero: true,
                      },
                      y: {
                        beginAtZero: true,
                        stacked: true,
                      }
            }

        },     
    })


    var chart = $('#oneChart'); 
    var jexcel = $('.draggable').height(); 

    chart.css('max-height', '300px');
    if (jexcel/1.8 > 300)
        chart.css('max-height', jexcel/1.8 +'px');  
} 