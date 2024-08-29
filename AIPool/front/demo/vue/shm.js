'use_strict';
var my_shm = {
    data() 
	{
	return {
		model: [
            {
                name: 'name',
                label: 'Название схемы',
                value: '',
                type: 'v-text-field',
                rules: [ value => {
                            if (value) return true;
                            return 'Название должно быть обязатель';
                        },
                ]//rule
            },
            {
                name: 'desc',
                label: 'Назначение и описание схемы',
                value: '',
                type: 'v-text-field',
            },
            {
                name: 'pool',
                label: 'К какому бассейну относится',
                value: '',
                type: 'v-select',
                choice: {
                    model: 'my_pool',
                    value: 'name',
                }
            }
            
        ]//model   
		}//
	},//data
    components: { crud },//components
    template: `<crud :model="model" :title="'Схемы бассейнов'"></crud>`
};//my_shm     