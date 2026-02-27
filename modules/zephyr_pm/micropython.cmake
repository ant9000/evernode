add_library(usermod_zephyr_pm INTERFACE)

target_sources(usermod_zephyr_pm INTERFACE
    ${CMAKE_CURRENT_LIST_DIR}/modzephyr_pm.c
)

target_include_directories(usermod_zephyr_pm INTERFACE
    ${CMAKE_CURRENT_LIST_DIR}
)

target_link_libraries(usermod INTERFACE usermod_zephyr_pm)
