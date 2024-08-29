let tv = {
    props:["pool"], 
    template: `#tv`, 
    methods: {
        full_load(){
            if (this.$store.getters.is_mobile && this.$store.getters.is_demo)
                this.$store.commit("settv");
            else
                this.$store.commit("showtv"); 
            
        },//full_load
    }//methods
}//tv


let all = {props:["pool"], template: `#all`,
    data: () => ({
         open: ['my_src', 'my_shm'],
         acts: [
                  {
                      icon: 'mdi-play',
                      name: 'play',
                      text: 'Открыть'
                  },
                  {
                      icon: 'mdi-link-variant',
                      name: 'show',
                      text: 'В новом'
                  },
                  {
                      icon: 'mdi-content-copy',
                      name: 'rtsp',
                      text: 'RTSP'
                  }
                ],
         groups: [
             {
                value: 'my_src',
                title: 'Видеопотоки',
             },
             {
                value: 'my_shm',
                title: 'Схемы',
             },
             
             ]
    }),//data
    methods:{
        urlflow_prev(type, pool, name){
            if ("{{test}}" == test)
                return 'https://cdn.vuetifyjs.com/images/parallax/material.jpg';
        },//urlflow_prev
        
        urlrtsp_prev(type, pool, name){
            if ("{{test}}" == test)
                return 'rtsp://';
        },//urlflow_prev
        
        action(act, type, item){
            if ('rtsp' == act) this.copy_rtsp(type, item);
            let url = `test/${item._id}.mp4`;
            //if ("{{test}}" != test) url = get_src_url(param);
            if ('play' == act) this.$store.commit("settv", [url, item]); 
            if ('show' == act) window.open(url, '_blank').focus();
           
        },//action
        
       
        
        copy_rtsp(type, item){
            let rtsp = `в демо версии нет rtsp`;
            if ("{{test}}" != test) rtsp = get_rtsp_url(type, item);
            if (!navigator.clipboard) return alert('Не поддерживается');
            navigator.clipboard.writeText(rtsp)
              .then(() => {})
              .catch(err => {console.log(err)});
              
        },//copy_rtsp
    }
}//all

let pool = {
    props:["pool"],
    
    components:{tv, all},
    template: `#pool`
}//pool

var home = {
    components:{pool},
    template: `#home`
}//home