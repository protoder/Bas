'use_strict';
var my_pool = {
    data() 
	{
	return {
		model: [
            {
                name: 'name',
                label: 'Название бассейна',
                value: '',
                type: 'v-text-field',
                rules: [ value => {
                            
                            if (undefined == value || '' == value) 
                                return 'Название должно быть обязатель';
                                
                            for (let item of this.$store.getters.list){
                                if (item.name == value && this.$store.state.item != item) 
                                    return 'Название должно быть отличным от других бассейнов';
                            }
                            
                            return true;
                        },
                    
                ]//rule
            },
            {
                name: 'desc',
                label: 'Описание',
                value: '',
                type: 'v-text-field',
            }
            
        ]//model   
		}//
	},//data
    components: {
	    'crud': crud,
	},//components
    template: `<crud :model="model" :title="'Список бассейнов'"></crud>`
};//my_pool     