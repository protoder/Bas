'use_strict';
var my_help = {
    data() 
	{
        return {
            desc: {
                
                my_pool: `В разделе меню "Бассейны" Вы добавляете бассейны их геометрические характеристики.`,
                my_src: `В разделе меню "Источники" Вы добавляете видеокамеры, которые направлены на бассейн(ы).
                Что бы добавить правильно видеокамеру, нужно указать адрес RTSP-потока камеры, принадлежность к бассейну и к какой схеме бассейна относится.`,
                my_shm: `В разделе меню "Схемы" Вы задаёте основные схемы для бассейна, что бы потом видеопотоки привязать к схеме бассйна.`,
                my_scr: `В разделе меню "Экраны" Вы управляете компоновкой отображения видеокамер и схем, задаете их положения относительно друг друга и размеры.`,
                my_opt: `Раздел "Параметры" отвечает за прочие настройки приложения`,
                my_home: `На главной странице отображаются ссылки на схемы бассейнов и их источники видео-потока.`,
            }
        }//return data
    },//data
    template: `#help`
};//my_help     


         