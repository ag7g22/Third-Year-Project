<template>
    <div class="container">
        <div v-if="state.current_view === 'selection'">
            <h1>{{ state.current_topic }}</h1>
            <div class="buttons-grid">
                <div v-for="clip in clips" :key="clip.name">
                    <button @click="load_video_clip(clip)">{{ clip.name }}</button>
                </div>
            </div>
            <div class="game-buttons">
                <button @click="next_page('hazard')" class="game-button">Back</button>
            </div>
        </div>
        <div v-if="state.current_view === 'video'" >
            <div v-if="too_many_clicks" class="overlay" @click="toggle_view('score')">
                <div class="overlay-content" @click.stop>
                    <h2>You've clicked too many times.</h2>
                    <p>(Click outside the box to move to the results screen.)</p>
                </div>
            </div>
            <div class="video-container">
                <video ref="hazard_perception"
                    :src="clip_url"
                    @click="handleClick"
                    @ended="finish_video_clip"
                    autoplay 
                    muted 
                    playsinline 
                    width="950"
                    height="650">
                </video>
                <!-- Click Effect -->
                <div 
                    v-for="(click, index) in clicks"
                    :key="index"
                    class="click-circle"
                    :style="{ top: (click.y - 10) + 'px', left: (click.x - 15) + 'px' }"
                ></div>
                <!-- Footer Section -->
                <div class="video-footer">
                    <div class="flags-container">
                        <div v-for="clicks in click_history" class="item">🚩</div>
                    </div>
                    <button @click="terminate_page()" class="game-button">Back</button>  
                </div>
            </div>
        </div>
        <div v-if="state.current_view === 'score'" class="questionnaire">
            <div class="quiz-result">
                <h1>You've completed the video! 🎉</h1>
                <h1> Score: {{ final_score }} / 5 </h1>
                <h2> {{ score_message }} </h2>
                <div class="game-buttons">
                   <button v-if="updateFinished" class="game-button" @click="terminate_page()">Back</button> 
                </div>
            </div>
        </div>
    </div>
</template>
  
<script>
import toastr from 'toastr';
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
            clip_url: '',

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
        exp_message() {
            if (this.exp_gain === 0) return;
            toastr.info(" ", `Gained ${this.exp_gain} exp!`, {
                closeButton: true,
                progressBar: true,
                positionClass: "toast-top-right",
                timeOut: 5000,
                showMethod: "fadeIn",
                hideMethod: "fadeOut",
                preventDuplicates: true
            });
        },
        level_up_message() {
            toastr.info(" ", "LEVELED UP!", {
                closeButton: true,
                progressBar: true,
                positionClass: "toast-top-right",
                timeOut: 5000,
                showMethod: "fadeIn",
                hideMethod: "fadeOut",
                preventDuplicates: true
            });
        },
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
        async load_video_clip(clip) {
            // Load the corrosponding clip
            console.log(clip.name);
            this.selected_clip = clip;
            const input = {'filename': clip.name + ".mp4"};

            const video = await this.azure_function('POST', '/question/get/video', input);
            if (video.result) {
                // Set the playing video
                this.clip_url = video.msg;
                console.log(this.clip_url);
                this.toggle_view('video');
            } else {
                this.message.error = video.msg || 'Loading video failed.'
            }
        },
        click_fail() {
            // Run this method if the user clicks more than 10 times
            const video = this.$refs.hazard_perception;
            video.pause();
            this.add_achievement('Where are you clicking lil bro','🚩');
            this.too_many_clicks = true;
            this.score_message = "Don't give up! Every attempt makes you better. Keep pushing forward!";
            this.message.success = "Gained no exp."
            this.updateFinished = true;
        },
        async finish_video_clip() {
            this.add_achievement('Eyes on the Road','💀');
            // Check if the user clicked on the appropriate (x,y) range:
            if ((this.click_x <= this.selected_clip.x + 50 && this.click_x >= this.selected_clip.x - 50) && 
                (this.click_y <= this.selected_clip.y + 50 && this.click_y >= this.selected_clip.y - 50)) {

                let interval = 1;

                // Then check if the user clicked at the right time:
                if (this.click_time >= this.selected_clip.time && this.click_time < this.selected_clip.time + interval) {
                    this.final_score = 5;
                    this.score_message = "Eagle eyed legend!";

                    if (this.selected_clip.name === "Urban Driving 5") {
                        this.add_achievement('Takin out the trash','🗑️');
                    } 
                    if (this.selected_clip.name === "Rural Driving 2") {
                        this.add_achievement('NEIGHHHHHH!','🐎');
                    } 
                    if (this.selected_clip.name === "Bigger Roads 1") {
                        this.add_achievement('Fireman sam','👨‍🚒');
                    } 
                    if (this.selected_clip.name === "Tricky Conditions 2") {
                        this.add_achievement('Oh deer','🦌');
                    } 
                    if (this.selected_clip.name === "Tricky Conditions 4") {
                        this.add_achievement('You snooze you lose!','💤');
                    } 
                    
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
            this.clip_url = '',
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
            if (update_response.result) {
                // Update rank in UI too.
                this.$store.commit("setCurrentRank", this.currentRank);
                this.currentRank = this.$store.state.currentRank;
                if (prev_level < this.currentRank.level) {
                    if (this.currentRank.level === 20) {
                        this.add_achievement('Absolute Bang out','🤓');
                    }
                    this.level_up_message();
                } else {
                    this.exp_message();
                }
            } else {
                this.message.error = update_response.msg || "Score update Failed."
            }
        },
        async add_achievement(name, emoji) {
            // Add an achievement in the user's data!
            if (this.$store.state.currentAchievements.includes(name)) {
                console.log("Already gotten the " + name + " achievement!")
                return;
            }
            const user_stats = this.$store.state.currentStats;
            const achievements = [...this.$store.state.currentAchievements, name];
            const input = { id: user_stats.id, updates: { achievements } };
            const update = await this.azure_function("PUT", "/user/update/info", input);
            if (update) {
                this.$store.commit("setCurrentAchievements", achievements);
                toastr.success(`${name} ${emoji}`, "Achievement Unlocked:", {
                closeButton: true,
                progressBar: true,
                positionClass: "toast-top-right",
                timeOut: 10000,
                showMethod: "fadeIn",
                hideMethod: "fadeOut"
                });
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
h1 {
    color: white;
}

.buttons-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr); /* Exactly 3 buttons per row */
  gap: 30px;
  padding: 20px;
}

.buttons-grid button {
    color: #f3af59;
    background-color: #424242;
    width: 100%;
    height: 150px;
    font-size: 1.2rem;
    cursor: pointer;
}

.buttons-grid button:hover {
    color: #dd9f4e;
    background-color: #343333;
}
</style>