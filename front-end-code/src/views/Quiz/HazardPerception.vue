<template>
    <div class="container">
        <h1 class="title">HAZARD PERCEPTION | {{ logged_in_user }}</h1>

        <div v-if="state.current_view === 'categories'" >
            <div class="instruction-box"> 
                <p> These are the different types of hazard perception clips as shown below. </p>
                <p> Try to get the correct clicked hazard! </p>
            </div>
            <div class="buttons">
                <button @click="init_quiz_instructions('Urban Driving')">Urban Driving</button>
                <button @click="init_quiz_instructions('Rural Driving')">Rural Driving</button>
                <button @click="init_quiz_instructions('Bigger Roads')">Bigger Roads</button>
                <button @click="init_quiz_instructions('Motorways')">Motorways</button>
            </div>

            <div class="buttons">
                <button @click="next_page('dashboard')">Back</button>
            </div>
        </div>

        <div v-if="state.current_view === 'instructions'">
            <div class="instruction-box"> 
                <h2 class="title">{{ this.state.current_topic }}: {{ this.state.current_description }}</h2>
                <p> You will be presented a driving video clip. </p>
                <p> Click at the area you believe there is a developing hazard </p>
                <p> and if you click again that will be your final answer. </p>
                <p> Select any of the clips to practice. </p>
            </div>

            <div class="buttons">
                <button @click="toggle_view('categories')">Back</button>
                <button @click="load_selection_screen()">Next</button>
            </div>
        </div>

        <p v-if="message.error" class="error-message">{{ message.error }}</p>
        <p v-if="message.success" class="success-message">{{ message.success }}</p>
    </div>
</template>
  
<script>
import toastr from 'toastr';
export default {
    // Page member variables and methods:
    name: "hazard",
    data() {
        return {
            state: { current_view: 'categories', current_topic: '', current_description: '' }, // State of quiz page
            logged_in_user: this.$store.state.currentUser,
            message: { error: "", success: "" },
        };
    },
    methods: {
        toggle_view(view) {
            // Reset state
            this.message.error = "";
            this.message.success = "";
            this.state.current_view = view;
        },
        init_quiz_instructions(topic) {
            // Reset messages
            this.message.error = "";
            this.message.success = "";

            // Initalise the quiz instructions
            this.state.current_topic = topic;

            switch (topic) {
                case 'Urban Driving':
                    this.state.current_description = 'driving in towns and cities.'
                    break;
                case 'Rural Driving':
                    this.state.current_description = 'driving in rural areas.'
                    break;
                case 'Bigger Roads':
                    this.state.current_description = 'driving in A roads and dual carriageways.'
                    break;
                case 'Motorways':
                    this.state.current_description = 'driving on the motorway.'
                    break;
            }
            
            this.toggle_view('instructions')
        },
        async add_achievement(name) {
            // Add achievement to user's achievements and notify on the UI.
            this.achievements.push(name)

            // Update database
            const input = { 'id': user_stats.id, 'updates': { 'achievements': this.achievements } }
            const update = await this.azure_function("PUT", "/user/update/info", input)
            if (update) {
                this.$store.commit("setCurrentAchievements", this.achievements);
                this.message.success = 'Achievements update Successful!'

                const options = { "closeButton": true, "debug": false, "newestOnTop": true, "progressBar": true,
                "positionClass": "toast-top-right", "preventDuplicates": true, "onclick": null, "showDuration": "300",
                "hideDuration": "1000", "timeOut": "5000", "extendedTimeOut": "1000", "showEasing": "swing",
                "hideEasing": "linear", "showMethod": "fadeIn","hideMethod": "fadeOut"}

                toastr.success('"' + `/${name}` + '""',"Achievement Unlocked:", options)
            }
        },
        async azure_function(function_type, function_route, json_doc) {
            console.log(function_route);
            // Call Azure function with request
            try {
                const url = process.env.VUE_APP_BACKEND_URL + function_route + '?code=' + process.env.VUE_APP_MASTER_KEY
                
                if (function_type === "GET") {
                    const response = await fetch( url, { method: function_type, headers: { "Content-Type": "application/json"} });
                    const API_reply = await response.json();
                    console.log("Result: " + JSON.stringify(API_reply.result));
                    return API_reply
                } else {
                    const response = await fetch( url, { method: function_type, headers: { "Content-Type": "application/json"},body: JSON.stringify(json_doc)});
                    const API_reply = await response.json();
                    console.log("Result: " + JSON.stringify(API_reply.result));
                    return API_reply
                }

            } catch (error) {
                console.error("Error:", error);
                this.message.error = "An API error occurred. Please try again later.";
            }
        },
        load_selection_screen() {
            // Load the videos according to the topic selected:
            let clips = [];

            switch (this.state.current_topic) {
                // Clips: (Video name, (x,y), time)
                case 'Urban Driving':
                    clips = [{name: 'Urban Driving 1', x: 370, y: 268, time: 15.25}];
                    break;
                case 'Rural Driving':
                    this.state.current_description = 'driving in rural areas.'
                    break;
                case 'Bigger Roads':
                    this.state.current_description = 'driving in A roads and dual carriageways.'
                    break;
                case 'Motorways':
                    this.state.current_description = 'driving on the motorway.'
                    break;
            }

            console.log("/HPvideo");
                this.$router.push({
                    path: `/HPvideo`,
                    query: { current_view: 'selection', current_topic: this.state.current_topic, clips: clips }
                });
        },
        next_page(page) {
            console.log("/" + page);
            this.$router.push(`/${page}`);
        }
    },
};
</script>

<style lang="scss" scoped>
.instruction-box {
  background-color: #f9f9f9;
  border-left: 5px solid #007bff;
  padding: 10px;
  margin: 10px 0;
  font-size: 14px;
  color: #333;
  border-radius: 5px;
}
</style>