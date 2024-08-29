'use_strict';
var my_scr = {
    data() 
	{
	return {
		model: [
            {
                name: 'name',
                label: 'Название экрана',
                value: '',
                type: 'v-text-field',
                target: 'title',
                rules: [ value => {
                            
                            if (undefined == value || '' == value) 
                                return 'Название должно быть обязатель';
                                
                            for (let item of this.$store.state[this.$store.state.content]){
                                if (item.name == value && this.$store.state.item != item) 
                                    return 'Название должно отличатся от других экранов';
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
                target: 'subtitle'
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
            }
            
        ]//model   
		}//
	},//data

    components: {
	    'crud': crud,
	},//components
    template: `<crud :model="model"></crud>`
};//my_scr     