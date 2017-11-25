var url = "http://127.0.0.1:8000/";

var user_id = null;
user_id = "";

var width = 540;
var height = 400;

function timeConvert(data) {
  return moment.unix(data).format("YYYY-MM-DD HH:mm:ss");
}

var orderCard = new Vue({
  el: '#orderCard',
  data: {
    type: 0,
    price: 0,
    amount: 0,
    total: 0,
    user_id : user_id,
    pre_user_id : ''
  },
  methods: {
    submit_id: function(){
      this.user_id = this.pre_user_id;
    },
    changePrice: function() {
      this.total = this.price * this.amount;
    },
    changeTotal: function() {
      this.amount = this.total / this.price;
    },
    changeType: function(type) {
      this.type = type;
    },
    sendMyOrder: function() {
      data = {
        user_id : user_id,
        token_id : 0,
        type : orderCard.type,
        price : orderCard.price,
        amount : orderCard.amount,
        timestamp : moment().unix()
      }
      $.ajax({
        type: 'POST',
        url: url+'order',
        data: data,
        crossDomain: true,
        success: this.showSuccess,
      });
    },
    showSuccess: function(data){
      $('#informationModal').modal()
    }
  }
});

var myOpenOrders = new Vue({
  el: '#myOpenOrders',
  data: {
    myOpenOrders: []
  },
  methods: {
    timeConvert: timeConvert
  }
});


var myTradeHistory = new Vue({
  el: '#myTradeHistory',
  data: {
    myTradeHistory: []
  },
  methods: {
    timeConvert: timeConvert
  }
});

var bidOrderBook = new Vue({
  el: '#bidOrderBook',
  data: {
    bidOrderBook: [],
    total: 0
  },
  methods: {
    timeConvert: timeConvert
  }
});

var sellOrderBook = new Vue({
  el: '#sellOrderBook',
  data: {
    sellOrderBook: [],
    total: 0
  },
  methods: {
    timeConvert: timeConvert
  }
});

function refreshData() {

  if(orderCard.user_id){
    $.ajax({
      url: url + "explorer/order/" + orderCard.user_id + "?" + "page_size=10000",
      crossDomain: true
    }).done(function(data) {
      myOpenOrders.myOpenOrders = data.order;
    });

    $.ajax({
      url: url + "explorer/trade/" + orderCard.user_id + "?" + "page_size=100000",
      crossDomain: true
    }).done(function(data) {
      myTradeHistory.myTradeHistory = data.order;
    });
}
  $.ajax({
    url: url + "explorer/order" + "?page_size=200&token_id=0",
    crossDomain: true,
  }).done(function(data) {
    sellOrderBook.sellOrderBook = data.sell.reverse();
    bidOrderBook.bidOrderBook = data.buy.reverse();
    sellOrderBook.total = data.total[0];
    bidOrderBook.total = data.total[1];
  });
$.ajax({
  url : url + "explorer/trade?token_id=0&until=10000000000",
  crossDomain: true
}).done(function(data){
    data.forEach(function(d){
        d.time = new Date(timeConvert(d.timestamp));
        d.price = d.price;
        d.total = d.total;
      });

      data = data.slice(data.length - 50,data.length);
      var margin = {top: 20, right: 45, bottom: 70, left: 45},
        width = 700 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom;
      var x = d3.scaleBand().range([0,width]).round(.05);
      var y1 = d3.scaleLinear().range([height, 0]);
      var y2 = d3.scaleLinear().range([height, 0]);
      var xAxis = d3.axisBottom(x).tickFormat(function(d){return d3.timeFormat("%H:%M:%S")(d)});
      var y1Axis = d3.axisLeft(y1).ticks(10);
      var y2Axis = d3.axisRight(y2).ticks(10);
      $("svg").empty();


      var svg = d3.select('svg')
      .append('g')
      .attr("transform",
             "translate(" + margin.left + "," + margin.top + ")");

             x.domain(data.map(function(d) { return d.time; }));
             y1.domain([0, d3.max(data, function(d) { return d.total; })*2]);
             y2.domain([0, d3.max(data, function(d) { return d.price; })*2]);

             svg.append("g")
                 .attr("class", "x axis")
                 .attr("transform", "translate(0," + height + ")")
                 .call(xAxis)
               .selectAll("text")
                 .style("text-anchor", "end")
                 .attr("dx", "-.8em")
                 .attr("dy", "-.55em")
                 .attr("transform", "rotate(-90)" );

             svg.append("g")
                 .attr("class", "y1 axis")
                 .call(y1Axis)
               .append("text")
                 .attr("transform", "rotate(-90)")
                 .attr("y", 6)
                 .attr("dy", ".71em")
                 .style("text-anchor", "end")
                 .text("Value ($)");

             svg.append("g")
                 .attr("class", "y2 axis")
                 .attr("transform", "translate(" + width + " ,0)")
                 .call(y2Axis)
               .append("text")
                 .attr("transform", "rotate(-90)")
                 .attr("y", 6)
                 .attr("dy", ".71em")
                 .style("text-anchor", "end")
                 .text("Value ($)");

             svg.selectAll("bar")
                 .data(data)
               .enter().append("rect")
                 .style("fill", "green")
                 .attr("x", function(d) { return x(d.time); })
                 .attr("width", x.bandwidth())
                 .attr("y", function(d) { return y1(d.total); })
                 .attr("height", function(d) { return height - y1(d.total); });


              var valueline = d3.line()
                  .x(function(d) { return x(d.time); })
                  .y(function(d) { return y2(d.price); });
            svg.append("path")
            .data([data])
            .attr("class", "line")
            .attr("d", valueline);

  });
}
setInterval(refreshData, 1000);
