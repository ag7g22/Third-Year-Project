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
                <h1>{{ state.current_topic }} {{ state.emoji }}</h1>
                <div class="description-box">
                    <p>{{ state.current_description }}</p>
                </div>
                <div class="game-buttons">
                    <button @click="toggle_view('categories')" class="game-button">Back</button>
                    <button @click="load_selection_screen()" class="game-button">Next</button>
                </div>
            </div>
        </div>
    </div>
</template>
  
<script>
export default {
    // Page member variables and methods:
    name: "hazard",
    data() {
        return {
            state: { current_view: 'categories', current_topic: '', current_description: '', emoji: '' }, // State of quiz page
            logged_in_user: this.$store.state.currentUser,
        };
    },
    methods: {
        toggle_view(view) {
            // Reset state
            this.state.current_view = view;
        },
        init_quiz_instructions(topic) {
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
        load_selection_screen() {
            // Load the videos according to the topic selected:
            let clips = [];

            switch (this.state.current_topic) {
                // Clips: (Video name, (x,y), time)
                case 'Urban Driving':
                    clips = [
                        {name: 'Urban Driving 1', x: 455, y: 335, time: 15.00},
                        {name: 'Urban Driving 2', x: 665, y: 330, time: 14.80},
                        {name: 'Urban Driving 3', x: 485, y: 325, time: 28.45},
                        {name: 'Urban Driving 4', x: 475, y: 325, time: 34.90},
                        {name: 'Urban Driving 5', x: 415, y: 345, time: 29.60}
                    ];
                    break;
                case 'Rural Driving':
                    clips = [
                        {name: 'Rural Driving 1', x: 620, y: 300, time: 47.65},
                        {name: 'Rural Driving 2', x: 280, y: 325, time: 31.00},
                        {name: 'Rural Driving 3', x: 475, y: 310, time: 18.70},
                        {name: 'Rural Driving 4', x: 530, y: 370, time: 13.90},
                        {name: 'Rural Driving 5', x: 350, y: 320, time: 38.85}
                    ];
                    break;
                case 'Bigger Roads':
                    clips = [
                        {name: 'Bigger Roads 1', x: 485, y: 320, time: 13.80},
                        {name: 'Bigger Roads 2', x: 485, y: 315, time: 14.50},
                        {name: 'Bigger Roads 3', x: 600, y: 320, time: 27.70},
                        {name: 'Bigger Roads 4', x: 590, y: 325, time: 22.00}
                    ];
                    break;
                case 'Motorways':
                    clips = [
                        {name: 'Motorways 1', x: 20, y: 263, time: 2.35},
                        {name: 'Motorways 2', x: 400, y: 325, time: 26.85},
                        {name: 'Motorways 3', x: 815, y: 360, time: 30.85}
                    ];
                    break;
                case 'Tricky Conditions':
                    clips = [
                        {name: 'Tricky Conditions 1', x: 165, y: 325, time: 17.10},
                        {name: 'Tricky Conditions 2', x: 600, y: 320, time: 31.90},
                        {name: 'Tricky Conditions 3', x: 510, y: 335, time: 33.20},
                        {name: 'Tricky Conditions 4', x: 400, y: 315, time: 23.50},
                        {name: 'Tricky Conditions 5', x: 375, y: 335, time: 25.83}
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