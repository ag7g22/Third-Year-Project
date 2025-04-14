<template>
    <div v-if="state.current_view === 'categories'" class="split-container">
        <div class="left-side">
            <div class="instructions-container">
                <h3>Now lets test your game senses ...</h3>
                <div class="feature-list">
                    <p>The hazard perception test checks how quickly you can spot developing dangers while driving. 
                        You'll watch video clips and click when you see a potential hazard. The faster you respond, the higher your score, 
                        helping prove you're alert and ready for real road situations.</p>
                </div>
                <h3>The hazard perception rules as follows:</h3>
                <div class="feature-list">
                    <p>- You have to click where you think is a developing hazard.</p>
                    <p>- The clicks will be recorded with a flag. 🚩</p>
                    <p>- If you click more than 10 times, you will be scored 0.</p>
                </div>
            </div>
        </div>
        <div class="right-side">
            <img src="@/assets/titles/HazardPerception.png" alt="Logo" class="task-logo"/>
            <div class="cat-buttons">
                <button @click="init_quiz_instructions('Urban Driving')">Urban Driving</button>
                <button @click="init_quiz_instructions('Rural Driving')">Rural Driving</button>
                <button @click="init_quiz_instructions('Bigger Roads')">Bigger Roads</button>
                <button @click="init_quiz_instructions('Motorways')">Motorways</button>
                <button @click="init_quiz_instructions('Tricky Conditions')">Tricky Conditions</button>
            </div>
            <div class="game-buttons">
                <button @click="next_page('dashboard')" class="game-button">Back</button>
            </div>
        </div>
    </div>
    <div v-else>
        <div v-if="state.current_view === 'instructions'" class="split-container">
            <div class="left-side">
                <div class="instructions-container">
                    <h3>now lets test your game senses ...</h3>
                    <div class="feature-list">
                        <p>The hazard perception test checks how quickly you can spot developing dangers while driving. 
                            You'll watch video clips and click when you see a potential hazard. The faster you respond, the higher your score, 
                            helping prove you're alert and ready for real road situations.</p>
                    </div>
                    <h3>The hazard perception rules as follows:</h3>
                    <div class="feature-list">
                        <p>- You have to click where you think is a developing hazard.</p>
                        <p>- The clicks will be recorded with a flag. 🚩</p>
                        <p>- If you click more than 10 times, you will be scored 0.</p>
                    </div>
                </div>
            </div>
            <div class="right-side">
                <h1>{{ state.current_topic }} {{ state.emoji }}</h1>
                <div class="description-box">
                    <p>{{ state.current_description }}</p>
                </div>
                <div class="game-buttons">
                    <button @click="toggle_view('categories')" class="game-button">Back</button>
                    <button @click="load_selection_screen()" class="game-button">Next</button>
                </div>
            </div>

            <p v-if="message.error" class="error-message">{{ message.error }}</p>
            <p v-if="message.success" class="success-message">{{ message.success }}</p>
        </div>
    </div>
</template>
  
<script>
import toastr from 'toastr';
export default {
    // Page member variables and methods:
    name: "hazard",
    data() {
        return {
            state: { current_view: 'categories', current_topic: '', current_description: '', emoji: '' }, // State of quiz page
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
                    this.state.emoji = '🏙️🚙';
                    this.state.current_description = "Hazard perception in urban driving involves staying alert in busy environments where hazards can appear suddenly—like pedestrians crossing, cars pulling out, or cyclists weaving through traffic. Being able to quickly spot and respond to these developing risks is crucial for safe driving in cities."
                    break;
                case 'Rural Driving':
                    this.state.emoji = '🌳🚘';
                    this.state.current_description = "Hazard perception in rural driving focuses on spotting less obvious dangers, such as sharp bends, hidden junctions, slow-moving farm vehicles, or animals crossing the road. These roads often have limited visibility and higher speeds, so reacting quickly to unexpected hazards is essential for safety."
                    break;
                case 'Bigger Roads':
                    this.state.emoji = '🛤️🚘';
                    this.state.current_description = "On bigger roads like A-roads and dual carriageways, hazard perception involves identifying fast-approaching risks such as sudden braking by other vehicles, merging traffic, or debris on the road. Since vehicles travel at higher speeds, early detection and quick response to developing hazards are crucial to avoid collisions and maintain safe driving."
                    break;
                case 'Motorways':
                    this.state.emoji = '🛣️🚙';
                    this.state.current_description = "In tricky conditions like rain, fog, snow, or nighttime, hazard perception becomes more challenging due to reduced visibility and lower grip on the road. Drivers must be extra alert for subtle cues such as brake lights, reflections, or changing road surfaces. Spotting hazards early in these conditions is essential for maintaining control and reacting in time to prevent accidents."
                    break;
                case 'Tricky Conditions':
                    this.state.emoji = '🌧️❄️';
                    this.state.current_description = "On motorways, hazard perception involves identifying risks at high speeds, such as sudden lane changes, slow-moving vehicles, or debris on the road. Because traffic moves quickly, early detection of developing hazards is crucial to allow for safe braking and lane adjustments. Staying alert and maintaining safe distances helps drivers respond calmly and effectively to any unexpected situations."
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
                    clips = [
                        {name: 'Urban Driving 1', x: 370, y: 270, time: 15.25},
                        {name: 'Urban Driving 2', x: 540, y: 270, time: 18.00},
                        {name: 'Urban Driving 3', x: 410, y: 260, time: 29.00},
                        {name: 'Urban Driving 4', x: 415, y: 260, time: 37.60},
                        {name: 'Urban Driving 5', x: 350, y: 260, time: 29.00}
                    ];
                    break;
                case 'Rural Driving':
                    clips = [
                        {name: 'Rural Driving 1', x: 490, y: 220, time: 47.00},
                        {name: 'Rural Driving 2', x: 250, y: 250, time: 31.00},
                        {name: 'Rural Driving 3', x: 395, y: 230, time: 17.50},
                        {name: 'Rural Driving 4', x: 450, y: 290, time: 13.45},
                        {name: 'Rural Driving 5', x: 295, y: 240, time: 37.85}
                    ];
                    break;
                case 'Bigger Roads':
                    clips = [
                        {name: 'Bigger Roads 1', x: 415, y: 250, time: 13.90},
                        {name: 'Bigger Roads 2', x: 425, y: 240, time: 14.55},
                        {name: 'Bigger Roads 3', x: 510, y: 260, time: 26.30},
                        {name: 'Bigger Roads 4', x: 500, y: 245, time: 21.45}
                    ];
                    break;
                case 'Motorways':
                    clips = [
                        {name: 'Motorways 1', x: 25, y: 190, time: 2.55},
                        {name: 'Motorways 2', x: 320, y: 250, time: 25.45},
                        {name: 'Motorways 3', x: 690, y: 290, time: 30.20}
                    ];
                    break;
                case 'Tricky Conditions':
                    clips = [
                        {name: 'Tricky Conditions 1', x: 110, y: 250, time: 17.10},
                        {name: 'Tricky Conditions 2', x: 515, y: 240, time: 31.80},
                        {name: 'Tricky Conditions 3', x: 280, y: 254, time: 33.45},
                        {name: 'Tricky Conditions 4', x: 325, y: 235, time: 22.70},
                        {name: 'Tricky Conditions 5', x: 320, y: 255, time: 24.00}
                    ];
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
</style>