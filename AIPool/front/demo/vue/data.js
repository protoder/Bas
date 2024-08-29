var data = {
  state () {
    return {
        tv:{
          show: false,
          src: null,
          title: 'Выберите видео для промотра',
          subtitle: ''
        },
        content: 'my_home',
        item: null,
        pools:{panel:[0]},
        menu: {
                
                my_home: { title: "Главная",   icon: "mdi-home"},
                my_pool: { title: "Бассейны",  icon: "mdi-pool"},
                my_shm:  { title: "Схемы",     icon: "mdi-map-marker-radius" },
                my_src:  { title: "Источники", icon: "mdi-video"},
                //my_scr:  { title: "Экраны",    icon: "fa-solid fa-desktop" },
                // my_opt:  { title: "Параметры", icon: "fa-solid fa-wrench"  },
                my_help: { title: "Справка",   icon: "mdi-help-circle"   },
                
            },//menu
        
        my_pool: [
                    {
                        _id: '12e12e1',
                        name: 'Тестовый бассейн',
                        desc: 'Этот бассейн для примера',
                    }
            ],//my_pool
        
        my_src: [
                {
                    _id:  'qwdqdwqq',
                    name: 'Тестовый видео-поток',
                    desc: 'Это тестовый адрес видео-потока для примера',
                    url:  'rtsp://admin:admin@127.0.0.1:554/live/main/',
                    pool: 'Тестовый бассейн',
                    shm: 'Схема главного потока',
                },
                {
                    _id:  'fhthjmnq',
                    name: 'Вторичный видео-поток',
                    desc: 'Тестовый видео-потока другого качества',
                    url:  'rtsp://admin:admin@127.0.0.1:554/live/sub/',
                    pool: 'Тестовый бассейн',
                    shm:  'Схема вторичного потока',
                }
            ],//my_src
            
        my_shm: [
                {
                     _id:  'dwdgdrew',
                    name: 'Схема главного потока',
                    desc: 'Более качественно, но дольше обработка',
                    pool: 'Тестовый бассейн'
                },
                {
                     _id:  'ddwdgdrew',
                    name: 'Схема вторичного потока',
                    desc: 'Точность ниже, зато оперативная обработка',
                    pool:  'Тестовый бассейн'
                }
            ],//my_shm    
        
        relations: {
            my_pool: [ ['my_src', 'pool'], ['my_shm', 'pool'] ],
            my_shm: [ ['my_src', 'shm']],
            //pool
        }
        
    }
  },//state
 
  getters:{
      list(state){
          return state[state.content];
      },//list
      bpoint(state){
	    return  window.innerWidth;
	 },//bpoint
	 is_full(state){
	     return null!=document.fullscreenElement;
	 },//is-full
	 is_mobile(state){
	     return window.innerWidth < 960;
	 },//is_mobile
	 is_demo(state){
	     return '{{test}}' == window.test;
	 }
  },//getters
  
  mutations: {
    
    show (state, content) {
        state.content = content;
        state.item = null;
    },//show
    showtv(state){
        if (!document.fullscreenElement) {
                document.documentElement.requestFullscreen();
                state.tv.show = true;
              } else if (document.exitFullscreen) {
                document.exitFullscreen();
                state.tv.show = false;
              }
    },//showtv
    
    settv(state, tv){
        try{
            let [url, item] = tv;
            state.tv.src = url;
            state.tv.title = item.name;
            state.tv.subtitle = item.desc;
        } catch (er) {}
        let video = document.getElementsByTagName('video');
        for (let v of video)v.load();
    },//settv
    
    current(state, name){
        for (let item of state[state.content]) {
            if (item.name == name){
                state.item = item;
            }
        }
    },//current
    
    remove(state){
        if (state.item._id == undefined) return;
            state[state.content] = state[state.content].filter(function(value, index, arr){ 
            return value._id != state.item._id;
        });
        state.item = null;
    },//remove
    
    update(state, model){
        
        if (state.item._id) {//Обновление
        
            for (let item of this.getters.list) {
                if (item._id != state.item._id) continue;
                for (let data of model){
                    this.commit("foreign", [state.content, data.name, data.value, item[data.name]]);
                    item[data.name] = data.value;
                }//for
            }//for
        }//Обновление
        else {//Добавление
            item = {_id: true};
            for (let data of model){
                item[data.name] = data.value;
            }
            this.getters.list.push(item);
        }
        state.item = null;
    },//update
    
    foreign(state, change){//fix внешних ключей
        const [name, key, cur, old] = change;
        let obj = state.relations[name];
        if (undefined == obj) return;
        
        for (const [model, key] of obj) {
            for (const item of state[model]){
                
                for (const k in item){
                    if (k != key) continue;
                    
                    if(item[k] == old)
                        item[k] = cur;
                }//for item
            }//for model
        }//for obj
            
    },//foreign
    
    
  },//mutations
  
}//data