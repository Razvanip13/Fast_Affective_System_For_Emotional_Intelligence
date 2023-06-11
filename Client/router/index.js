import Vue from 'vue'
import VueRouter from 'vue-router'
// import Home from '../views/Home.vue'
// import Dummy from "../components/Dummy";
import LoginView from "../views/LoginView";
import MenuView from "../views/MenuView";
import TestsListView from "../views/TestsListView";
import TestView from "../views/TestView";
import ResultsListView from "../views/ResultsListView";
import ChartListView from "../views/ChartListView";
Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'LoginView',
    component: LoginView
  },
  {
    path: '/:id/menu/',
    name: 'MenuView',
    component: MenuView
  },
  {
    path: '/:id/tests',
    name: 'TestsListView',
    component: TestsListView
  },
  {
    name: 'TestView',
    path:'/:idUser/tests/:idTest',
    component: TestView
  },
  {
    path: '/:id/results',
    name: 'ResultsListView',
    component: ResultsListView
  },
  {
    path: '/:id/charts',
    name: 'ChartListView',
    component: ChartListView
  },



]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
