window.dash_clientside = Object.assign({}, window.dash_clientside, {
    test: {
        update_log: function() {
            console.log(dash_clientside.callback_context);
            const triggered_id = dash_clientside.callback_context.triggered_id;
            return "triggered id: " + triggered_id
        },
        create_chart: function(figure, scale) {
            if(figure === undefined) {
                return {'data': [], 'layout': {}};
            }
            const fig = Object.assign({}, figure, {
                'layout': {
                    'yaxis': {
                         'type': scale,
                    },
                    'xaxis':{
                        'title':'Year'
                    },
                    'title':'GapminderDataFiveYear',
                 }
            });
            return fig;
        },
        async_fetch: async function(value) {
            const response = await fetch(value);
            const data = await response.json();
            return data;
        },
        change_template: function(switchOn){
           document.documentElement.setAttribute('data-bs-theme', switchOn ? 'light' : 'dark');

           return window.dash_clientside.no_update
        },


    }
});


