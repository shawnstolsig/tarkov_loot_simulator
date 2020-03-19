<template>
    <v-app-bar app clipped-left>
        
        <!-- Site logo/title -->
        <v-img 
            :src="require('@/assets/logo.png')"
            contain
            max-height="64"
            max-width="200"
        ></v-img>
        <v-toolbar-title>Loot Trainer</v-toolbar-title>

        <v-spacer></v-spacer>
    
        <!-- Toolbar buttons -->
        <v-toolbar-items>
            <v-btn text to="/" class="mr-2">
                <span>Home</span>
                <v-icon right>mdi-home</v-icon>
            </v-btn>
            <v-btn text to="/admin" class="mr-2">
                <span>Admin</span>
                <v-icon right>mdi-shield-account</v-icon>
            </v-btn>
            <v-btn text to="/about" class="mr-2">
                <span>About</span>
                <v-icon right >mdi-information</v-icon>
            </v-btn>
        </v-toolbar-items>
    </v-app-bar>
</template>


<script>


export default {
    data(){
        return {
         
        }
    },  // end data
    methods: {
        
    },  // end methods
    computed: {
       
    }   // end computed
}
</script>