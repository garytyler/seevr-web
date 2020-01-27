import Vue from "vue";
import VueRouter from "vue-router";
import UserApp from "@/views/UserApp.vue";
import GuestApp from "@/views/GuestApp.vue";
// import Error404ResourceNotFound from "@/views/Error404ResourceNotFound.vue";
// import Error404PageNotFound from "@/views/Error404PageNotFound.vue";
import Error404NotFound from "@/views/Error404NotFound.vue";
import store from "@/store";

Vue.use(VueRouter);

var loadFeatureBeforeRouterEnter = function(to, from, next) {
  sessionStorage.setItem("key1", "value1");
  console.log(sessionStorage.getItem("key1"));
  store
    .dispatch("guest_app/loadFeature", to.params.feature_slug)
    .then(function() {
      next();
    })
    .catch(error => {
      let message = `Feature not found: ${error.config.url}`;
      next(`/not-found/?message=${message}`);
    });
};

const routes = [
  {
    path: "/",
    name: "user",
    component: UserApp,
    props: true
  },
  {
    path: "/feature/:feature_slug",
    name: "guest-app",
    component: GuestApp,
    beforeEnter: loadFeatureBeforeRouterEnter
  },
  {
    path: "/not-found",
    name: "resource-not-found",
    component: Error404NotFound,
    props: route => ({ message: route.query.message })
  },
  {
    path: "*",
    name: "page-not-found",
    component: Error404NotFound,
    props: { message: "Page Not Found" }
  }
];

const router = new VueRouter({
  mode: "history",
  routes
});

export default router;
