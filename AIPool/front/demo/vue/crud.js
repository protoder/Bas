'use_strict';
let edit = {
    template: `#edit`, 
    props: ["model"],
    emits: ["submit"],
    computed:{
        value(){
            let obj = {};
            for (let item of this.model)
                obj[item.name] = item.value;
            return obj;
        }
    },//computed
    methods:{
        choice(f){
            if (undefined == f.choice) return [];
            return this.$store.state[f.choice.model]
            .filter( e=> (undefined == f.choice.relation) || (e[f.choice.relation] == this.value[f.choice.relation]) )
            .map(e=>e[f.choice.value]);
        }
    },//methods
    
};//edit

let list = {
    template: `#list`, 
    props: ["title"],
    emits: ["add"]
};

var crud = {
    props: ["model", "title"],
    components:{list, edit},
    computed: {
        item () {
            return this.$store.state.item;
        }
    },//computed
    watch: {
        item (cur, old) {
            if (null == cur) return;
            for (let item of this.model)
                if (cur[item.name] != undefined)
                    item.value = cur[item.name];
        }
    },//watch
     methods:{
        add(){
            this.$store.state.item = {}; 
            this.model.forEach(e=>e.value = undefined);
        },
        submit(form){
            form.validate().then(r => {
                if (!r.valid) return;
                this.$store.commit('update', this.model);
            })
        },
     },//methods
    template: `<edit v-if="$store.state.item" @submit="submit" :model="model"></edit>
    <list v-else :title="title" @add="add"></list>`
};//crud     