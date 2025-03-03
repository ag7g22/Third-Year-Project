<template>
    <div class="container">

        <div v-if="state.current_view === 'selection'">
            <h1 class="title">HAZARD PERCEPTION | {{ state.current_topic }} | {{ logged_in_user }}</h1>

            <div class="buttons">
                <div v-for="clip in clips">
                    <button @click="load_video_clip(clip)">{{ clip.name }}</button>
                </div>
            </div>

            <button @click="next_page('hazard')">Back</button>
        </div>

        <div v-if="state.current_view === 'video'" class="video-container">
            <div>
                <video ref="hazard_perception"
                    :src="playing_video[0]?.src"
                    @click="handleClick"
                    @ended="finish_video_clip"
                    autoplay 
                    muted 
                    playsinline 
                    width="800"
                    height="500">
                </video>

                <!-- Click Effect -->
                <div 
                    v-for="(click, index) in clicks"
                    :key="index"
                    class="click-circle"
                    :style="{ top: (click.y - 10) + 'px', left: (click.x - 15) + 'px' }"
                ></div>
            </div>

            <div v-if="too_many_clicks" class="overlay">
                <div class="overlay-content" @click.stop>
                    <p>You've clicked too many times.</p>
                    <button @click="toggle_view('score')">Next</button>
                </div>
            </div>
            
            <div class="horizontal-container">
                <div v-for="clicks in click_history" class="item">🚩</div>
            </div>

            <div class="buttons">
                <button @click="terminate_page()">Back</button>  
            </div>
        </div>

        <div v-if="state.current_view === 'score'">
            <h1 class="title">HAZARD PERCEPTION | {{ state.current_topic }} | {{ logged_in_user }}</h1>
            <div class="score">
                <h2>You've completed the video! 🎉</h2>
                <h3> Score: {{ final_score }} / 5 </h3>
                <p> {{ score_message }} </p>
                <button v-if="updateFinished" class="stop-button" @click="terminate_page()">Back</button>
            </div>
        </div>

        <p v-if="message.error" class="error-message">{{ message.error }}</p>
        <p v-if="message.success" class="success-message">{{ message.success }}</p>
    </div>
</template>
  
<script>
import toastr from 'toastr';
const videoContext = require.context('@/assets/videos', false, /\.mp4$/);
const videos = videoContext.keys().map(key => ({
  src: videoContext(key),
  title: key.replace('./', '').replace('.mp4', '') // Clean filename
}));

export default {
    // Page member variables and methods:
    name: "HPvideo",
    mounted() {
        this.state = { current_view: this.$route.query.current_view, current_topic: this.$route.query.current_topic } || { current_view: 'selection', current_topic: '' }
        this.clips = this.$route.query.clips
    },
    data() {
        return {
            state: { current_view: 'selection', current_topic: '' }, // State of hazard page

            // Clips
            clips: [],
            selected_clip: null,
            playing_video: null,

            // Clicking the video
            click_x: 0,
            click_y: 0,
            click_time: 0,
            click_history: [],
            clicks: [],
            too_many_clicks: false,

            // Final score:
            final_score: 0,
            score_message: "",
            exp_gain: 0,

            // Flag for updating database scores.
            updateFinished: false,

            logged_in_user: this.$store.state.currentUser,
            currentRank: this.$store.state.currentRank,
            message: { error: "", success: "" },
        };
    },
    methods: {
        handleClick(event) {
            // This method records when and where in the video you clicked.
            const video = this.$refs.hazard_perception;

            if (this.click_history.length > 10) {
                this.click_fail();
            }

            // Get click position relative to the video element
            this.click_x = (event.offsetX).toFixed(2);
            this.click_y = (event.offsetY).toFixed(2);

            // Get the timestamp of the click
            this.click_time = video.currentTime.toFixed(2);

            // Store in history
            this.click_history.push({
                x: this.click_x,
                y: this.click_y,
                time: this.click_time,
            });

            console.log(
                `Clicked at X: ${this.click_x}, Y: ${this.click_y}, Time: ${this.click_time}s`
            );

            // Add click animation
            this.clicks.push({ x: this.click_x, y: this.click_y});

            // Remove animation after 0.3s
            setTimeout(() => {
                this.clicks.shift();
            }, 600);

        },
        toggle_view(view) {
            // Reset state
            this.state.current_view = view;
        },
        load_video_clip(clip) {
            // Load the corrosponding clip
            console.log(clip.name)
            this.selected_clip = clip;
            this.playing_video = videos.filter(video => video.title.includes(clip.name));
            this.toggle_view('video');
        },
        click_fail() {
            // Run this method if the user clicks more than 10 times
            const video = this.$refs.hazard_perception;
            video.pause();
            this.too_many_clicks = true;
            this.score_message = "Don't give up! Every attempt makes you better. Keep pushing forward!";
            this.message.success = "Gained no exp."
            this.updateFinished = true;
        },
        async finish_video_clip() {

            // Check if the user clicked on the appropriate (x,y) range:
            if ((this.click_x <= this.selected_clip.x + 50 && this.click_x >= this.selected_clip.x - 50) && 
                (this.click_y <= this.selected_clip.y + 50 && this.click_y >= this.selected_clip.y - 50)) {

                let interval = 1;

                // Then check if the user clicked at the right time:
                if (this.click_time >= this.selected_clip.time && this.click_time < this.selected_clip.time + interval) {
                    this.final_score = 5;
                    this.score_message = "Eagle eyed legend!";
                    this.exp_gain = 350;
                } else if (this.click_time >= this.selected_clip.time + interval && this.click_time < this.selected_clip.time + interval*2) {
                    this.final_score = 4;
                    this.score_message = "You almost got it, keep trying!";
                    this.exp_gain = 280;
                } else if (this.click_time >= this.selected_clip.time + interval*2 && this.click_time < this.selected_clip.time + interval*3) {
                    this.final_score = 3;
                    this.score_message = "This is pretty good, you can do better!";
                    this.exp_gain = 210;
                } else if (this.click_time >= this.selected_clip.time + interval*3 && this.click_time < this.selected_clip.time + interval*4) {
                    this.final_score = 2;
                    this.score_message = "You're learning, and that's what matters! Keep challenging yourself!";
                    this.exp_gain = 140;
                } else if (this.click_time >= this.selected_clip.time + interval*4 && this.click_time < this.selected_clip.time + interval*5) {
                    this.final_score = 1;
                    this.score_message = "Not bad! Mistakes help us grow—review what you missed and try again!";
                    this.exp_gain = 70;
                } else {
                    this.final_score = 0;
                    this.score_message = "Don't give up! Every attempt makes you better. Keep pushing forward!";
                }

            } else {
                this.score_message = "Don't give up! Every attempt makes you better. Keep pushing forward!";
            }

            this.toggle_view('score');

            if (this.final_score >= 1) {
                console.log('Got a score!')
                await this.update_user_exp();
                this.updateFinished = true;
            } else {
                console.log('No score!')
                this.message.error = "Gained no exp."
                this.updateFinished = true;
            }

        },
        terminate_page() {
            // Reset variables
            this.selected_clip = null;
            this.playing_video = null;
            this.toggle_view('selection');
            this.click_x = 0;
            this.click_y = 0;
            this.click_time = 0;
            this.click_history = [];
            this.clicks = [];
            this.too_many_clicks = false;
            this.final_score = 0;
            this.score_message = "";
            this.exp_gain = 0;
            this.updateFinished = false;
            this.message = { error: "", success: "" }
        },
        async update_user_exp() {
            // Add changes to database
            const user_stats = this.$store.state.currentStats;
            const prev_level = this.currentRank.level;

            // Increment level if exp exceeds threshold:
            if (this.currentRank.exp + this.exp_gain >= this.currentRank.exp_threshold) {
                // Reset exp progress but add leftover exp and update exp threshold
                this.currentRank.exp = (this.currentRank.exp + this.exp_gain) - this.currentRank.exp_threshold;
                this.currentRank.level += 1;
                this.currentRank.exp_threshold += 500;
            } else {
                this.currentRank.exp += this.exp_gain;
            }

            const input = { id: user_stats.id, updates: { "rank": this.currentRank } };
            console.log(input);

            const update_response = await this.azure_function("PUT", "/user/update/info", input)
            // Show message incase the API response fails, otherwise update state.
            if (update_response.result) {
                // Update rank in UI too.
                this.$store.commit("setCurrentRank", this.currentRank);
                this.currentRank = this.$store.state.currentRank;
            
                if (prev_level < this.currentRank.level) {
                    this.message.success = `LEVELED UP TO LEVEL ${this.currentRank.level}!` 
                } else {
                    this.message.success = `Gained ${this.exp_gain} exp!`
                }

            } else {
                this.message.error = update_response.msg || "Score update Failed."
            }
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
        next_page(page) {
            console.log("/" + page);
            this.$router.push(`/${page}`);
        }
    },
};
</script>

<style lang="scss" scoped>
.video-container {
  position: relative;
  display: inline-block;
}

/* Animated Click Circle */
.click-circle {
  position: absolute;
  width: 30px;
  height: 30px;
  background-color: rgba(237, 18, 18, 0.8);
  border-radius: 50%;
  transform: translate(-50%, -50%);
  animation: clickEffect 0.6s ease-out forwards;
}

@keyframes clickEffect {
  0% {
    transform: scale(0);
    opacity: 1;
  }
  100% {
    transform: scale(2);
    opacity: 0;
  }
}

.horizontal-container {
    display: flex; /* Display items in a row */
    gap: 10px; /* Optional: Adds space between the items */
}

.item {
    width: 20px; /* Set width */
    height: 20px; /* Set height */
    padding: 10px;
    border-radius: 4px;
}

.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7); /* Semi-transparent background */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

/* Centered box but slightly above the middle */
.overlay-content {
  background: white;
  padding: 20px;
  border-radius: 10px;
  text-align: center;
  width: 80%;
  max-width: 400px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
}

.score {
  text-align: center;
  max-width: 500px;
  margin: auto;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  background: #f9f9f9;
}

</style>