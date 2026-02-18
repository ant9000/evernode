set(MICROPY_PORT_DIR ${APP_DIR})
set(MICROPY_DIR      ${APP_DIR}/../../)
set(TARGET           ${APPLICATION_BINARY_DIR})

target_include_directories(app PRIVATE ${MICROPY_DIR} ${MICROPY_PORT_DIR} ${TARGET})
target_link_directories(app PRIVATE ${TARGET})
target_link_libraries(app PRIVATE micropython)

target_sources(app PRIVATE src/modmachine_bare_metal_funcs.c)
