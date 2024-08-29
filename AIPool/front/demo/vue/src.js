'use_strict';
var my_src = {
    data() 
	{
	return {
	    title: 'Адреса источников видео',
		model: [
            {
                name: 'name',
                label: 'Название источника',
                value: '',
                type: 'v-text-field',
                rules: [ value => {
                            if (undefined == value || '' == value) 
                                return 'Название должно быть обязатель';
                                
                            for (let item of this.$store.getters.list){
                                if (item.name == value && this.$store.state.item != item) 
                                    return 'Название должно отличатся от других видео-потоков';
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
            },
            {
                name: 'url',
                label: 'URL-адрес',
                value: '',
                type: 'v-text-field',
                rules: [ value => {
                            if (value) return true;
                            return 'Адрес должен быть задан';
                        },
                ]//rule
            },
            {
                name: 'pool',
                label: 'Бассейн',
                value: '',
                type: 'v-select',
                choice: {
                    model: 'my_pool',
                    value: 'name'
                }
            },
            {
                name: 'shm',
                label: 'Схема',
                value: '',
                type: 'v-select',
                choice: {
                    model: 'my_shm',
                    value: 'name',
                    relation: 'pool'
                }
            }
            
        ]//model   
		}//
	},//data
    components: {
	    'crud': crud,
	},//components
    template: `<crud :model="model" :title="title"></crud>`
};//my_src     