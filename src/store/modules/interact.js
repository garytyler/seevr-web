import axios from "axios";

const state = {
  feature: null,
  sessionGuest: null
};

const getters = {
  feature(state) {
    return state.feature;
  },
  featureSlug(state) {
    return state.feature ? state.feature.slug : null;
  },
  featureTitle(state) {
    return state.feature ? state.feature.title : null;
  },
  featureGuests(state) {
    return state.feature ? state.feature.guests : null;
  },
  featurePresenterChannel(state) {
    return state.feature ? state.feature.presenter_channel : null;
  },
  isFeaturePresenterOnline(state) {
    return Boolean(state.feature?.presenter_channel?.length > 0);
  },
  sessionGuest(state) {
    return state.sessionGuest;
  },
  sessionGuestId(state) {
    return state.sessionGuest ? state.sessionGuest.id : null;
  },
  sessionGuestName(state) {
    return state.sessionGuest?.name;
  },
  interactingGuest(state) {
    return state.feature?.guests?.length ? state.feature.guests[0] : null;
  },
  interactingGuestId(state) {
    return state.feature?.guests?.length ? state.feature.guests[0].id : null;
  }
};

const mutations = {
  SET_FEATURE(state, feature) {
    state.feature = feature;
  },
  UPDATE_FEATURE(state, feature) {
    state.feature = { ...state.feature, ...feature };
  },
  SET_SESSION_GUEST(state, sessionGuest) {
    state.sessionGuest = sessionGuest;
  },
  DELETE_GUEST(state, guest_id) {
    state.feature.guests.filter(i => i.id != guest_id);
  }
};

const actions = {
  loadFeature({ commit }, slug) {
    return new Promise((resolve, reject) => {
      axios
        .get(`/api/features/${slug}/`)
        .then(response => {
          commit("SET_FEATURE", response.data);
          resolve(response.data);
        })
        .catch(error => {
          reject(error);
        });
    });
  },
  loadSessionGuest({ commit }) {
    return new Promise((resolve, reject) => {
      axios
        .get(`/api/feature/${state.feature.slug}/guest/`)
        .then(response => {
          if (response.status == 200) {
            commit("SET_SESSION_GUEST", response.data);
            resolve(response.data);
          } else {
            reject(response.error);
          }
        })
        .catch(error => {
          reject(error);
        });
    });
  },
  setSessionGuest({ commit }, sessionGuest) {
    return new Promise((resolve, reject) => {
      axios
        .post(`/api/feature/${state.feature.slug}/guest/`, sessionGuest)
        .then(response => {
          if (response.status == 200) {
            commit("SET_SESSION_GUEST", response.data);
            resolve(response.data);
          } else {
            reject(response.error);
          }
        })
        .catch(error => {
          reject(error);
        });
    });
  },
  updateGuest({ commit, state }, guest) {
    return new Promise((resolve, reject) => {
      axios
        .patch(`/api/feature/${state.feature.slug}/guest/${guest.id}/`, guest)
        .then(response => {
          if (response.status == 200) {
            commit("SET_SESSION_GUEST", response.data);
            resolve(response.data);
          } else {
            reject(response.error);
          }
        })
        .catch(error => {
          reject(error);
        });
    });
  },
  deleteGuest({ commit, state }, guestId) {
    return new Promise((resolve, reject) => {
      axios
        .delete(`/api/feature/${state.feature.slug}/guest/${guestId}/`)
        .then(response => {
          if (response.status == 204) {
            commit("DELETE_GUEST", state.feature, guestId);
            resolve(response.data);
          } else {
            reject(response.error);
          }
        })
        .catch(error => {
          reject(error);
        });
    });
  },
  // Websocket receivers
  receiveFeature({ commit }, data) {
    commit("SET_FEATURE", data.feature);
  }
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
};