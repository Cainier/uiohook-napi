{
  'targets': [
    {
      'target_name': 'uiohook_napi',
      'dependencies': ['libuiohook'],
      'sources': [
        'src/lib/addon.c',
        'src/lib/napi_helpers.c',
        'src/lib/uiohook_worker.c',
      ],
      'include_dirs': [
        'libuiohook/include',
        'src/lib',
      ],
      'conditions': [
        ['OS=="mac"', {
          # Build universal2 binary for Electron cross-arch packaging on Apple Silicon
          'xcode_settings': {
            'ARCHS': ['arm64', 'x86_64'],
            'ONLY_ACTIVE_ARCH': 'NO',
            'MACOSX_DEPLOYMENT_TARGET': '10.13'
          },
          'cflags+': ['-arch', 'arm64', '-arch', 'x86_64'],
          'ldflags+': ['-arch', 'arm64', '-arch', 'x86_64']
        }]
      ]
    },
    {
      'target_name': 'libuiohook',
      'type': 'static_library',
      'sources': [
        'libuiohook/src/logger.c',
      ],
      'include_dirs': [
        'libuiohook/include',
        'libuiohook/src',
      ],
      "conditions": [
        ['OS=="win"', {
          'sources': [
            'libuiohook/src/windows/input_helper.c',
            'libuiohook/src/windows/input_hook.c',
            'libuiohook/src/windows/post_event.c',
            'libuiohook/src/windows/system_properties.c'
          ],
          'include_dirs': [
            'libuiohook/src/windows'
          ]
        }],
        ['OS=="linux"', {
          'defines': [
            'USE_XRANDR', 'USE_EVDEV', 'USE_XT'
          ],
          'link_settings': {
            'libraries': [
              '-lX11', '-lXrandr', '-lXtst', '-lpthread', '-lXt'
            ],
          },
          'cflags': ['-std=c99', '-pedantic', '-Wall', '-pthread'],
          'sources': [
            'libuiohook/src/x11/input_helper.c',
            'libuiohook/src/x11/input_hook.c',
            'libuiohook/src/x11/post_event.c',
            'libuiohook/src/x11/system_properties.c'
          ],
          'include_dirs': [
            'libuiohook/src/x11'
          ]
        }],
        ['OS=="mac"', {
          "defines":[
            "__MACOSX_CORE__","USE_IOKIT","USE_APPLICATION_SERVICES","USE_OBJC"
          ],
          "link_settings": {
            "libraries": [
              "-framework IOKit",
              "-framework Carbon",
              "-framework ApplicationServices",
              "-framework AppKit",
              "-framework CoreFoundation"
            ],
          },
          'xcode_settings': {
            'ARCHS': ['arm64', 'x86_64'],
            'ONLY_ACTIVE_ARCH': 'NO',
            'MACOSX_DEPLOYMENT_TARGET': '10.13'
          },
          'cflags': ['-std=c99', '-pedantic', '-Wall', '-pthread', '-arch', 'arm64', '-arch', 'x86_64'],
          'ldflags': ['-arch', 'arm64', '-arch', 'x86_64'],
          'sources': [
            "libuiohook/src/darwin/input_helper.c",
            "libuiohook/src/darwin/input_hook.c",
            "libuiohook/src/darwin/post_event.c",
            "libuiohook/src/darwin/system_properties.c"
          ],
          'include_dirs': [
            'libuiohook/src/darwin'
          ]
        }]
      ]
    }
  ]
}
